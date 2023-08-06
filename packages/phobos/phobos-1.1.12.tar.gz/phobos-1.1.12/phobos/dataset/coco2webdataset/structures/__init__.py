from .bounding_box import BoxList
from .segmentation_mask import SegmentationMask
from .keypoint import PersonKeypoints
from .utils import interpolate

__all__ = ['BoxList','SegmentationMask','PersonKeypoints','interpolate']