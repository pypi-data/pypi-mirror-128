from torch.utils.data import DataLoader
from torch.utils.data.distributed import DistributedSampler

import torch.distributed as dist
import webdataset as wds

def urlSampler(url,rank,world_size):
    front, out = url.split('{')
    out, back = out.split('}')
    m, n = out.split('..')
    index_len = len(m)
    m,n = int(m),int(n)
    sz = n-m+1
    print(world_size,sz)
    assert world_size <= sz, "Total URL tars are less than world_size"
    sz_ = int(sz // world_size)
    #smart sampling 
    remainder = sz-sz_*world_size
    cond = world_size-remainder
    start_ind = rank*sz_+m
    end_ind = (rank+1)*sz_+m-1
    if rank >= cond:
        gap=rank-cond
        start_ind += gap
        end_ind += gap+1

    return f"{front}{'{'}{str(start_ind).zfill(index_len)}..{str(end_ind).zfill(index_len)}{'}'}{back}"
    
    


def getWdsDistLoader(
    train_posix,
    val_posix,
    batch_size,
    num_workers,
    train_transform=None,
    val_transform=None,
    shuffle=True,
    distributed=False,
    distributed_val=True
):
    """
    
    Creates distributed dataloader:-
        For train_dataset: assigns distributed sampler,
        For val_dataset: assigns distributed sampler for distributed val step i.e. args.val_node=-1, else sampler=None

    Parameters
    ----------
    train_posix : `torch.utils.data.Dataset <https://pytorch.org/docs/stable/data.html#torch.utils.data.Dataset>`_
        train_dataset
    val_posix : `torch.utils.data.Dataset <https://pytorch.org/docs/stable/data.html#torch.utils.data.Dataset>`_
        val_dataset
    args : `dict <https://docs.python.org/3/tutorial/datastructures.html#dictionaries>`_
        args.train
            args.train['batch_size'] : `int <https://docs.python.org/3/library/functions.html#int>`_, 
            args.train['num_workers'] : `int <https://docs.python.org/3/library/functions.html#int>`_
        args.val
            args.val['batch_size'] : `int <https://docs.python.org/3/library/functions.html#int>`_, 
            args.val['num_workers'] : `int <https://docs.python.org/3/library/functions.html#int>`_
        args.distributed : `boolean <https://docs.python.org/3/library/functions.html#bool>`_
            distributed
        args.val_node : `int <https://docs.python.org/3/library/functions.html#int>`_
            val_node
    
    Examples
    --------
    Create distributed train and val loaders from DummyPreLoader instances

    >>> def get_train_val_metadata(args):
    ...     train_metadata = [1, 2]
    ...     val_metadata = [3, 4]
    ...     return train_metadata, val_metadata
    >>> 
    >>> class DummyPreloader(torch.utils.data.Dataset):
    ...     def __init__(self, metadata, args=None):
    ...         random.shuffle(metadata)
    ...         self.samples = metadata
    ...         self.args = args
    ...
    ...     def __getitem__(self, index):
    ...         return np.random.randn(1, 32, 32), np.zeros(32, 32)
    ...
    ...     def __len__(self):
    ...         return len(self.samples)
    >>>
    >>> train_samples, val_samples = get_train_val_metadata(args)
    >>> 
    >>> train_dataset = DummyPreloader(train_samples, args)
    >>> val_dataset = DummyPreloader(val_samples, args)
    >>>
    >>> train_loader, val_loader = getDistLoaders(
    ...                                 train_dataset,
    ...                                 val_dataset,
    ...                                 batch_size=args.batch_size,
    ...                                 num_workers=args.num_workers,
    ...                                 distributed=args.distributed,
    ...                                 distributed_val=args.distributed_val
    ...                                 )
    
    """

    train_posix_,val_posix_ = None,None

    if distributed:
        train_posix_ = urlSampler(train_posix,dist.get_rank(),dist.get_world_size())
        if distributed_val:
            val_posix_ = urlSampler(val_posix,dist.get_rank(),dist.get_world_size())
    # loaders
    if not train_posix_:
        train_posix_ = train_posix
    if not val_posix_:
        val_posix_ = val_posix
    if train_transform:
        train_dataset = (wds.Dataset(train_posix_)
            .shuffle(shuffle)
            .decode()
            .map(train_transform)
            )
    else:
        train_dataset = (wds.Dataset(train_posix_)
            .shuffle(shuffle)
            .decode()
            )
    if val_transform:
        val_dataset = (wds.Dataset(val_posix_)
            .shuffle(False)
            .decode()
            .map(val_transform)
        )
    else:
        val_dataset = (wds.Dataset(val_posix_)
            .shuffle(False)
            .decode()
        )
    train_loader = DataLoader(
        train_dataset,
        batch_size=batch_size,
        num_workers=num_workers,
        pin_memory=True
    )
    val_loader = DataLoader(
        val_dataset,
        batch_size=batch_size,
        num_workers=num_workers,
        pin_memory=True
    )
    return train_loader, val_loader
