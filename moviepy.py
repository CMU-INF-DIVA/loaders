import numpy as np
import torch

from moviepy.editor import VideoFileClip

from .base import Frame, FrameBatch, Loader


class MoviePyLoader(Loader):

    def __init__(self, video_path, parent_dir=''):
        super().__init__(video_path, parent_dir)
        self.video = VideoFileClip(self.path, audio=False)
        self.set_meta(self.video.fps, self.video.size[0], self.video.size[1],
                      self.video.duration * self.video.fps)

    def __call__(self, batch_size=1, limit=None, stride=1, start=0):
        frames = []
        batch_id = 0
        if limit is not None:
            end = min(start + limit * stride, self.meta.num_frames)
        else:
            end = self.meta.num_frames
        frame_ids = np.arange(start, end, stride)
        for frame_id in frame_ids:
            image = self.video.get_frame(frame_id / self.meta.frame_rate)
            frame = Frame(np.ascontiguousarray(image[:, :, ::-1]), frame_id)
            frames.append(frame)
            if len(frames) == batch_size:
                yield FrameBatch(frames, batch_id)
                frames = []
                batch_id += 1
        if len(frames) > 0:
            yield FrameBatch(frames, batch_id)
