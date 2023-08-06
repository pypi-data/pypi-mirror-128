import os
import webdataset as wds
import math
import pickle
import json
import glob
import tqdm
import time

from webdataset import ShardWriter
from torch.utils.data import Dataset, DataLoader


def toHHMMSS(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    
    return "%d:%02d:%02d" % (hour, minutes, seconds)


class Dataset2WebDataset:
    r"""
    Creates Posix Tar shards for DataStore(datastore.granular.ai) for torch.utils.data.Dataset

    Here, key_names should be in

        **class** :         ["cls", "cls2", "class", "count", "index", "inx", "id"]
    
        **text** :          ["txt", "text", "transcript"]
    
        **image** :         ["png", "jpg", "jpeg", "img", "image", "pbm", "pgm", "ppm"]

        **image_path** :    ["path"]

        **bytes** :         ["bytes"]
    
        **pickle_object** : ["pyd", "pickle"]
    
        **torch_object** :  ["pth"]
    
        **numpy.ndarray** : ["npy"]  don't use not stable
    
        **json_dict** :     ["json", "jsn"]

    Parameters
    ----------
    dataset : `torch.utils.data.Dataset <https://pytorch.org/docs/stable/data.html#torch.utils.data.Dataset>`_
        Dataset to convert
    key_names : `list <https://docs.python.org/3/tutorial/introduction.html#lists>`_
        Ordered list for the items returned by the input dataset iterator
    transforms : `object <https://docs.python.org/3/reference/datamodel.html#objects-values-and-types>`_
        Transforms object to be saved on datastore for the input dataset
    mode : `str <https://docs.python.org/3/library/stdtypes.html#str>`_
        Dataset mode type = train/val/test
    shard_size : `int <https://docs.python.org/3/library/functions.html#int>`_
        Upper bound on shard memory size in GBs, default = 10GB

    Examples
    --------
    Please check `here <https://github.com/granularai/phobos/blob/develop/examples/dataset2wds/Example.ipynb>`_ 

    """
    def __init__(self, 
            dataset: Dataset, 
            keys: list, 
            transforms: object, 
            mode:str = 'train', 
            shard_size = 10,
            shard_size_bytes=None
            ) -> None:
        self.keys = keys
        self.dataset = dataset
        self.mode = mode
        self.transforms = transforms
        self.index_len = int(math.log10(len(self.dataset)))+1 if len(self.dataset) > 0 else 1
        if not shard_size_bytes:
            shard_size = Dataset2WebDataset.shardSizeToBytes(shard_size)
        else:
            shard_size = shard_size_bytes
        sz_,self.time_per_shard = Dataset2WebDataset.getSampleSize(self.dataset, self.keys, self.index_len)
        self.sample_size = sz_
        self.samples_per_shard = int(shard_size // sz_)

        print(f"samples_per_shard:{self.samples_per_shard} sample_size_bytes:{self.sample_size}, ETA: {toHHMMSS(len(self.dataset)*self.time_per_shard)}")

    @staticmethod
    def getBytes(path):
        with open(path, 'rb') as fp:
            return fp.read()

    @staticmethod
    def getBytesLen(stream):
        return len(stream)
    
    @staticmethod
    def shardSizeToBytes(shard_size):
        shard_dec = shard_size - shard_size//1
        shard_dec = math.ceil(shard_dec*1000)
        shard_dec = (shard_dec << 10) << 10
        shard_size = int(shard_size)
        shard_size = ((shard_size//1 << 10) << 10) << 10
        shard_size += shard_dec
        return shard_size

    @staticmethod
    def getSampleSize(dataset, keys, index_len):
        index = 1
        time_elapsed = time.time()
        items = dataset[0]
        with ShardWriter('tmp-%01d.tar', maxcount=1) as sink:
            sample = {
                "__key__": str(index).zfill(index_len)
            }
            for key, val in zip(keys, items):
                if type(val) == str and key.split('.')[-1] == "path":
                    val = Dataset2WebDataset.getBytes(val)
                sample[key] = val
            sink.write(sample)
        time_elapsed = time.time()-time_elapsed
        with open("tmp-0.tar", 'rb') as fp:
            fp.seek(0, os.SEEK_END)
            sz_ = fp.tell()
        os.remove("tmp-0.tar")     
        return sz_, time_elapsed
    
    @staticmethod
    def getShardSize(dataset,nodes,keys,max_shard_size):
        max_shard_size_bytes = Dataset2WebDataset.shardSizeToBytes(max_shard_size)
        index_len = int(math.log10(len(dataset)))+1 if len(dataset) > 0 else 1
        sample_sz,_ = Dataset2WebDataset.getSampleSize(dataset, keys, index_len)
        dataset_samples_sz = (len(dataset)*sample_sz) // nodes
        if dataset_samples_sz >= max_shard_size_bytes:
            res = Dataset2WebDataset.shardSizeToBytes(max_shard_size)
        else:
            res = dataset_samples_sz
        return res

    def writeShards2Local(self,shuffle=True, out_path:str = "./",num_workers=1):
        r"""
        Writes shards on local filesystem

        Parameters
        ----------
        out_path : `str <https://docs.python.org/3/library/stdtypes.html#str>`_
            Output path for writing shards
        """
        data_loader = DataLoader(
            self.dataset,
            batch_size=1,
            shuffle=shuffle,
            num_workers=num_workers
        )

        dataset_ln = len(self.dataset)

        shards_out = out_path+"/"+f"{self.mode}-%0{self.index_len}d.tar"
        with ShardWriterCustom(shards_out, 
            maxcount = self.samples_per_shard) as sink:
            progress_bar = tqdm.tqdm(enumerate(data_loader))
            for index, items in progress_bar:
                sample = {
                    "__key__" : str(index).zfill(self.index_len)
                }
                for key,val in zip(self.keys,items):
                    val=val[0]
                    if type(val) == str and key.split('.')[-1] == "path":
                        val = Dataset2WebDataset.getBytes(val)
                    sample[key] = val
                sink.write(sample)
                progress_bar.set_description(f"Writing {self.mode} shards, In progress : {(index+1)}/{dataset_ln}, ETA: {toHHMMSS((dataset_ln-index-1)*self.time_per_shard)}")
                if index == len(self.dataset)-1:
                    break
        transform_out = out_path +"/transforms.pkl"
        if self.transforms is not None:
            with open(transform_out,'wb') as fp:
                pickle.dump(self.transforms,fp)
        metadata_out = out_path + f"/metadata_{self.mode}.json"
        tar_last = sorted(glob.glob(os.path.join(out_path,self.mode+"-*.tar")))[-1].split('-')[-1].split('.')[0]
        with open(metadata_out, 'w') as fp:
            json.dump({
                "transforms": "transforms.pkl",
                "url_posix_path": self.mode+"-{"+str(0).zfill(
                    self.index_len)+".."+tar_last+"}.tar",
                "mode": self.mode,
                "shards_count": int(tar_last)+1,
                "num_samples": len(self.dataset),
                "keys": self.keys,
                "samples_per_shard": self.samples_per_shard
            }, fp)

    @classmethod
    def trainVal2Shards(
        cls,
        train_dataset,
        val_dataset,
        keys,
        distributed_val=True,
        mode='node',
        val=16,
        max_shard_size=2,
        shuffle=True,
        dst='./',
        train_transform=None,
        val_transform=None
    ):
        '''mode = node/size'''
        if mode == 'node':
            val = int(val)
        if not os.path.exists(dst):
            print("output directory does not exist")
            return
        else:
            paths = []
            for path in ['train','val']:
                tmp = os.path.join(dst,path)
                if not os.path.exists(tmp):
                    os.makedirs(tmp)
                paths.append(tmp)
            train_path, val_path = paths

        
        if mode == 'node':
            nodes = val
            assert len(train_dataset) >= nodes and len(val_dataset) >= nodes
            train_shard_size = Dataset2WebDataset.getShardSize(train_dataset,nodes,keys,max_shard_size)
            if distributed_val:
                val_shard_size = Dataset2WebDataset.getShardSize(val_dataset,nodes,keys,max_shard_size)
            else:
                val_shard_size = Dataset2WebDataset.shardSizeToBytes(max_shard_size)
        else:
            train_shard_size = Dataset2WebDataset.shardSizeToBytes(val)
            val_shard_size = Dataset2WebDataset.shardSizeToBytes(val)

        train = cls(train_dataset,keys,mode='train',shard_size_bytes=train_shard_size,transforms=train_transform)
        val = cls(val_dataset,keys,mode='val',shard_size_bytes=val_shard_size,transforms=val_transform)
        print("writing train shards")
        train.writeShards2Local(shuffle=shuffle, out_path=train_path)
        print("writing val shards")
        val.writeShards2Local(shuffle=False,out_path=val_path)
        print("Completed!")


class ShardWriterCustom(ShardWriter):
    def __init__(self, pattern, maxcount, **kw):
        super(ShardWriterCustom,self).__init__(pattern, maxcount=maxcount, **kw)

    def write(self,obj):
        """Write a sample.
        :param obj: sample to be written
        """
        if self.tarstream is None or self.count >= self.maxcount:
            self.next_stream()
        size = self.tarstream.write(obj)
        self.count += 1
        self.total += 1
        self.size += size