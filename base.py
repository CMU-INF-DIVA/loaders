import os.path as osp
from collections import namedtuple
from typing import Iterator, List, Tuple, Union

import numpy as np
import torch


class Frame(object):

    def __init__(self, image: np.ndarray, frame_id: int,
                 sequence_id: Union[None, int] = None):
        '''
        image: numpy array as H x W x C[BGR] in [0, 256)
        frame_id: raw index in the original video
        sequence_id: actual index in the current load. 
            None for the same as frame_id.
        '''
        self.image = torch.as_tensor(image)
        self.frame_id = frame_id
        self.sequence_id = sequence_id or frame_id


LoaderMeta = namedtuple('LoaderMeta', [
    'frame_rate', 'width', 'height', 'num_frames'])


class Loader(object):

    def __init__(self, video_path: str, parent_dir: str = ''):
        self.path = osp.join(parent_dir, video_path)

    def set_meta(self, frame_rate: float, width: int, height: int,
                 num_frames: Union[None, int] = None):
        self.meta = LoaderMeta(
            float(frame_rate), int(width), int(height), num_frames)

    def __call__(self, batch_size: int = 1, limit: Union[None, int] = None,
                 stride: int = 1,  start: int = 0) \
            -> Iterator[List[Frame]]:
        '''
        batch_size: number of frames in a batch
        limit: total number of frames to yield
        stride: gap between adjacent frames, 1 for no skip
        start: frame_id of the first frame
        '''
        raise NotImplementedError

    def __repr__(self):
        return '%s.%s@%s' % (
            self.__module__, self.__class__.__name__, self.path)
