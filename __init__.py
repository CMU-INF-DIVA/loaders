__author__ = 'Lijun Yu'

from .base import Frame, FrameBatch


def get_loader(name):
    if name == 'AVI-R':
        from .avi_r import AVIRLoader
        return AVIRLoader
    elif name == 'Decord':
        from .decord import DecordLoader
        return DecordLoader
    elif name == 'MoviePy':
        from .moviepy import MoviePyLoader
        return MoviePyLoader
    elif name == 'OpenCV':
        from .opencv import OpenCVLoader
        return OpenCVLoader
    else:
        raise NotImplementedError('Loader<%s> not found' % (name))
