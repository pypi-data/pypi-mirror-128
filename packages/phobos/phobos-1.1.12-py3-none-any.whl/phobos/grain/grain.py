from inspect import getmodule
from yacs.config import CfgNode as CN
from yacs import config
from polyaxon.tracking import Run

import logging
import os
import yaml
import copy

config._VALID_TYPES = config._VALID_TYPES.union({Run})

_VALID_TYPES = config._VALID_TYPES


class Grain(CN):
    """A class derived from class CfgNode from yacs which can
    be used for creating python yacs object from yaml.
    These arguments can be obtained from:
    1. YAML config file
    Grain can also be used to load arguments for models
    and log model inputs
    Parameters
    ----------
    polyaxon_exp : `polyaxon.tracking.Run <https://polyaxon.com/docs/experimentation/tracking/client/>`_
        polyaxon experiment
    *args : `list <https://docs.python.org/3/tutorial/introduction.html#lists>`_
        a non keyworded arguments' list.
    **kwargs : `dict <https://docs.python.org/3/tutorial/datastructures.html#dictionaries>`_
        a keyworded arguments' list.
    Attributes
    ----------
    The object formed is a nested YACS object hence the YAML keys converts into multilevel keys/attributes.
    polyaxon_exp : `polyaxon.tracking.Run <https://polyaxon.com/docs/experimentation/tracking/client/>`_
        polyaxon experiment
    Examples
    --------
    1. Parsing dummy CLI arguments through a default Grain instance
    >>> grain_exp = Grain()
    >>> args.input_shape
    [1, 16, 16, 2]
    2. Parsing dummy CLI arguments through a Grain instance linked to a polyaxon experiment
    >>> from polyaxon.tracking import Run
    >>> experiment = Run()
    >>> grain_exp = Grain(polyaxon_exp=experiment)
    >>> args = grain_exp.parse_args(['--sensor', 'dummy',
    ...                              '--band_ids', 'gray',
    ...                              '--input_shape', '1,16,16,2',
    ...                              '--resolution', '1'])
    >>> args.input_shape
    [1, 16, 16, 2]
    3. Parsing dummy metadata JSON through a Grain instance
    >>> grain_exp = Grain()
    >>> args = grain_exp.parse_args_from_yaml('/tmp/metadata.yaml')
    >>> args.sensor
    'sentinel2'
    4. Load a dummy model through Grain instance
    >>> class DummyNet(nn.Module):
    ... def __init__(self, foo):
    ...     super(DummyNet, self).__init__()
    ...     self.layer = foo
    ...
    ... def forward(self, x):
    ...     return x
    >>>
    >>> grain_exp = Grain()
    >>> model = grain_exp.load_model(DummyNet, foo='bar')
    >>> model.layer
    'bar'
    """
    def __init__(self, polyaxon_exp = None, *args, **kwargs):
        super(Grain,self).__init__(*args, **kwargs)
        self.polyaxon_exp = polyaxon_exp
    
    
    def parse_args_from_yaml(self, yaml_file):
        with open(yaml_file,'r') as fp:
            _ = yaml.safe_load(fp.read())
            _ = Grain._create_config_tree_from_dict(_,key_list=[])
            super(Grain, self).__init__(init_dict = _)
            if self.polyaxon_exp:
                self.polyaxon_exp.log_inputs(
                    convert_to_dict(self,[])
                )
        return self
    

    def load_model(self, model_cls, **kwargs):
        """Log and instantiate a model with keyword arguments

        Parameters
        ----------
        model_cls : `torch.nn.module <https://pytorch.org/docs/stable/generated/torch.nn.Module.html>`_
            A pytorch model class to instantiate.
        **kwargs : `dict <https://docs.python.org/3/tutorial/datastructures.html#dictionaries>`_
            all model positional arguments

        Returns
        -------
        `object <https://docs.python.org/3/reference/datamodel.html#objects-values-and-types>`_
            pytorch model object created from keyword arguments.

        """
        logging.debug("Enter load_model routine")
        if self.polyaxon_exp:
            self._log_model(model_cls, **kwargs)
        logging.debug("Exit load_model routine")
        return model_cls(**kwargs)

    def _log_model(self, model_cls, **kwargs):
        """Log model inputs

        Parameters
        ----------
        model_cls : `torch.nn.module <https://pytorch.org/docs/stable/generated/torch.nn.Module.html>`_
            A pytorch model class.
        **kwargs : `dict <https://docs.python.org/3/tutorial/datastructures.html#dictionaries>`_
            all model positional arguments

        """
        logging.debug("Enter _log_model routine")
        model_module = getmodule(model_cls).__name__
        model_path = os.path.relpath(getmodule(model_cls).__file__)
        model_name = model_cls.__name__

        self.polyaxon_exp.log_inputs(model_path=model_path,
                                     model_name=model_name,
                                     model_module=model_module,
                                     model_args=kwargs)
        logging.debug("Exit _log_model routine")
        
    @classmethod
    def _create_config_tree_from_dict(cls, dic, key_list):
        """
        Create a configuration tree using the given dict.
        Any dict-like objects inside dict will be treated as a new CfgNode.
        Args:
            dic (dict):
            key_list (list[str]): a list of names which index this CfgNode from the root.
                Currently only used for logging purposes.
        """
        dic = copy.deepcopy(dic)
        for k, v in dic.items():
            if isinstance(v, dict):
                # Convert dict to CfgNode
                dic[k] = CN(v, key_list=key_list + [k])
            else:
                # Check for valid leaf type or nested CfgNode
                _assert_with_logging(
                    _valid_type(v, allow_cfg_node=False),
                    "Key {} with value {} is not a valid type; valid types: {}".format(
                        ".".join(key_list + [str(k)]), type(v), _VALID_TYPES
                    ),
                )
        return dic

def convert_to_dict(cfg_node, key_list):
    if not isinstance(cfg_node, CN):
        return cfg_node
    else:
        cfg_dict = dict(cfg_node)
        for k, v in cfg_dict.items():
            cfg_dict[k] = convert_to_dict(v, key_list + [k])
        return cfg_dict

def _assert_with_logging(cond, msg):
    if not cond:
        logging.debug(msg)
    assert cond, msg

def _valid_type(value, allow_cfg_node=False):
    return (type(value) in _VALID_TYPES) or (
        allow_cfg_node and isinstance(value, CN)
    )
