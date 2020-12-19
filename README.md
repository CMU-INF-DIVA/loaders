# Loaders

Author: Lijun Yu

Email: lijun@lj-y.com

A submodule of video loaders.

## Loaders

* [AVI-R](https://pypi.org/project/avi-r/) for `.avi` files only (handles missing frames).
* [MoviePy](https://pypi.org/project/moviepy/) for `.mp4` and other files.
* [Decord](https://github.com/dmlc/decord).
* [OpenCV](https://opencv.org).

## API

```python
from loaders import get_loader

video_path = ...
loader_class = get_loader('AVI-R')  # Or MoviePy, Decord, OpenCV

loader = loader_class(video_path)
for frame_batch in loader(): # Optional params: start=0, end=None, stride=1, batch_size=1
    # Do something with the frame batch

loader.close()  # Release resources
```

## Dependency

See [actev_base](https://github.com/CMU-INF-DIVA/actev_base).

## License

See [License](LICENSE).
