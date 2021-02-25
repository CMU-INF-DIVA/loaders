import numpy as np

from decord import VideoReader

from .base import Frame, FrameBatch, Loader


class DecordLoader(Loader):

    def __init__(self, video_path, parent_dir='', **reader_args):
        super().__init__(video_path, parent_dir)
        self.video = VideoReader(self.path, **reader_args)
        height, width = self.video[0].shape[:2]
        self.set_meta(self.video.get_avg_fps(), width, height, len(self.video))

    def __call__(self, start=0, end=None, stride=1, batch_size=1):
        end = end or self.meta.num_frames
        frames = []
        batch_id = 0
        self.video.seek_accurate(start)
        for frame_id in range(start, end, stride):
            image = self.video.next().asnumpy()
            frame = Frame(np.ascontiguousarray(image[:, :, ::-1]), frame_id)
            frames.append(frame)
            if len(frames) == batch_size:
                yield FrameBatch(frames, batch_id)
                frames = []
                batch_id += 1
            if stride > 1:
                self.video.skip_frames(stride - 1)
        if len(frames) > 0:
            yield FrameBatch(frames, batch_id)

    def close(self):
        del self.video
