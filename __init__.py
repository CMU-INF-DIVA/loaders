__author__ = 'Lijun Yu'


def get(name):
    if name == 'AVI-R':
        from .avi_r import AVIRLoader
        return AVIRLoader
    else:
        raise NotImplementedError('Loader<%s> not found' % (name))
