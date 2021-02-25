import numpy as np

from moviepy.editor import VideoFileClip

from .base import Frame, FrameBatch, Loader


class MoviePyLoader(Loader):

    def __init__(self, video_path, parent_dir='', **reader_args):
        super().__init__(video_path, parent_dir)
        self.video = VideoFileClip(self.path, audio=False, **reader_args)
        self.set_meta(self.video.fps, self.video.size[0], self.video.size[1],
                      self.video.duration * self.video.fps)

    def __call__(self, start=0, end=None, stride=1, batch_size=1):
        end = end or self.meta.num_frames
        frames = []
        batch_id = 0
        for frame_id in range(start, end, stride):
            image = self.video.get_frame(frame_id / self.meta.frame_rate)
            frame = Frame(np.ascontiguousarray(image[:, :, ::-1]), frame_id)
            frames.append(frame)
            if len(frames) == batch_size:
                yield FrameBatch(frames, batch_id)
                frames = []
                batch_id += 1
        if len(frames) > 0:
            yield FrameBatch(frames, batch_id)

    def close(self):
        self.video.close()
