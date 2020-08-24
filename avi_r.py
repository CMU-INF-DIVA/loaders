import numpy as np
import torch

from avi_r import AVIReader

from .base import Frame, FrameBatch, Loader


class AVIRLoader(Loader):

    def __init__(self, video_path, parent_dir=''):
        super().__init__(video_path, parent_dir)
        self.video = AVIReader(video_path, parent_dir)
        self.set_meta(self.video.frame_rate, self.video.width,
                      self.video.height, self.video.num_frames)

    def __call__(self, batch_size=1, limit=None, stride=1, start=0):
        frames = []
        batch_id = 0
        self.video.seek(start)
        for raw_frame in self.video.get_iter(limit, stride):
            frame = Frame(raw_frame.numpy('bgr24'), raw_frame.frame_id)
            frames.append(frame)
            if len(frames) == batch_size:
                yield FrameBatch(frames, batch_id)
                frames = []
                batch_id += 1
        if len(frames) > 0:
            yield FrameBatch(frames, batch_id)

    def close(self):
        self.video.close()
