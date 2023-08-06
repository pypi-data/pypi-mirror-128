import io
import json
from torch.utils.data import Dataset

from phobos.dataset.coco2webdataset import COCODataset
from phobos.dataset.dataset2wds import Dataset2WebDataset

class ProcDataset(Dataset):
    def __init__(self, coco_dataset):
        super(ProcDataset, self).__init__()
        self.coco = coco_dataset
        _,target,_ = self.coco[0]
        keys = ['x.img.id','x.category.id','x.jpeg']
        keys.append("y.bbox.xyxy.pth")
        keys.append("y.bbox.xywh.pth")
        if target.has_field('masks'):
            keys.append(f"y.masks.json.bin")
        self.keys = keys
    def __len__(self):
        return self.coco.__len__()
    def __getitem__(self, index):
        img,target,idx = self.coco[index]
        out = [idx]
        out.append(target.get_field('labels'))
        with io.BytesIO() as stream:
            img.save(stream,format='JPEG',quality=100)
            out.append(stream.getvalue())
        out.append(target.convert(mode='xyxy').bbox)
        out.append(target.convert(mode='xywh').bbox)
        if target.has_field('masks'):
            masks = target.get_field("masks")
            seg_mask = {'segmentation':[]}
            for polygon in masks.instances.polygons:
                seg_mask['segmentation'].append(polygon.polygons[0].numpy().tolist())
            out.append(json.dumps(seg_mask))
        
        return out



        

def coco2wds(
        train_img_dir,
        train_anno_file,
        val_img_dir,
        val_anno_file,
        img_size,
        mode='node',
        val=16,
        max_shard_size=1,
        shuffle=True,
        dst='./',
        distributed_val=True
    ):
        train_coco = COCODataset(
            train_anno_file,
            train_img_dir,
            True,
            img_size
        )
        val_coco = COCODataset(
            val_anno_file,
            val_img_dir,
            True,
            img_size
        )
        train_dataset = ProcDataset(train_coco)
        keys = train_dataset.keys
        val_dataset = ProcDataset(val_coco)
        
        Dataset2WebDataset.trainVal2Shards(
            train_dataset,
            val_dataset,
            keys,
            distributed_val,
            mode,
            val,
            max_shard_size,
            shuffle,
            dst
        )