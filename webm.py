import av

from .base import Frame, FrameBatch, Loader


class WebmLoader(Loader):

    def __init__(self, video_path, parent_dir=''):
        super().__init__(video_path, parent_dir)
        self.video = av.open(self.path)
        self.stream = self.video.streams.video[0]
        self.set_meta(
            float(self.stream.average_rate),
            self.stream.codec_context.format.width,
            self.stream.codec_context.format.height, int(1e6))

    def __call__(self, batch_size=1, limit=None, stride=1, start=0):
        frames = []
        batch_id = 0
        assert start == 0 and limit is None
        frame_id = -1
        for raw_frame in self.video.decode(video=0):
            frame_id += 1
            if frame_id % stride != 0:
                continue
            frame = Frame(raw_frame.to_ndarray(format='bgr24'), frame_id)
            frames.append(frame)
            if len(frames) == batch_size:
                yield FrameBatch(frames, batch_id)
                frames = []
                batch_id += 1
        if len(frames) > 0:
            yield FrameBatch(frames, batch_id)

    def close(self):
        self.video.close()
        del self.video, self.stream
