import cv2

from .base import Frame, FrameBatch, Loader


class OpenCVLoader(Loader):

    def __init__(self, video_path, parent_dir=''):
        super().__init__(video_path, parent_dir)
        self.video = cv2.VideoCapture(self.path)
        assert self.video.isOpened(), 'Video not found: %s' % (self.path)
        self.set_meta(
            self.video.get(cv2.CAP_PROP_FPS),
            self.video.get(cv2.CAP_PROP_FRAME_WIDTH),
            self.video.get(cv2.CAP_PROP_FRAME_HEIGHT),
            self.video.get(cv2.CAP_PROP_FRAME_COUNT))

    def __call__(self, start=0, end=None, stride=1, batch_size=1):
        end = end or self.meta.num_frames
        frames = []
        batch_id = 0
        self.video.set(cv2.CAP_PROP_POS_FRAMES, start)
        for frame_id in range(start, end, stride):
            ret, image = self.video.read()
            if not ret:
                break
            frame = Frame(image, frame_id)
            frames.append(frame)
            if len(frames) == batch_size:
                yield FrameBatch(frames, batch_id)
                frames = []
                batch_id += 1
            for _ in range(stride - 1):
                ret, _ = self.video.read()
                if not ret:
                    break
        if len(frames) > 0:
            yield FrameBatch(frames, batch_id)

    def close(self):
        self.video.release()
