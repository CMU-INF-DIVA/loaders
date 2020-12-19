import os.path as osp
from collections import namedtuple
from typing import Iterator, List, Union

import numpy as np
import torch


class Frame(object):

    def __init__(self, image: np.ndarray, frame_id: int, **custom_attributes):
        '''
        image: numpy array as H x W x C[BGR] in [0, 256)
        frame_id: frame index in the original video
        '''
        self.image = torch.as_tensor(image)
        self.frame_id = frame_id
        self.__dict__.update(custom_attributes)

    def __repr__(self):
        return '%s(id=%d)' % (self.__class__.__name__, self.frame_id)


class FrameBatch(object):

    def __init__(self, frames: List[Frame], batch_id: int,
                 **custom_attributes):
        self.frame_class = type(frames[0])
        self.images = [frame.image for frame in frames]
        self.frame_ids = torch.as_tensor([frame.frame_id for frame in frames])
        self.batch_id = batch_id
        self.__dict__.update(custom_attributes)

    def __len__(self):
        return self.frame_ids.shape[0]

    def __repr__(self):
        return '%s(id=%d, len=%d, range=%d-%d)' % (
            self.__class__.__name__, self.batch_id, len(self),
            self.frame_ids[0], self.frame_ids[-1])


LoaderMeta = namedtuple('LoaderMeta', [
    'frame_rate', 'width', 'height', 'num_frames'])


class Loader(object):

    def __init__(self, video_path: str, parent_dir: str = ''):
        self.path = osp.join(parent_dir, video_path)

    def set_meta(self, frame_rate: float, width: int, height: int,
                 num_frames: Union[None, int] = None):
        self.meta = LoaderMeta(
            float(frame_rate), int(width), int(height),
            int(num_frames) if num_frames is not None else None)

    def __call__(self, start: int = 0, end: Union[None, int] = None,
                 stride: int = 1, batch_size: int = 1) \
            -> Iterator[FrameBatch]:
        '''
        start: frame_id of the first frame
        end: frame_id of the frame after the last frame
        stride: gap between adjacent frames, 1 for no skip
        batch_size: number of frames in a batch
        '''
        raise NotImplementedError

    def close(self):
        return

    def __repr__(self):
        return '%s.%s@%s' % (
            self.__module__, self.__class__.__name__, self.path)
