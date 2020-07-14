# Loaders

Author: Lijun Yu

Email: lijun@lj-y.com

A submodule of video loaders.

## Loaders

* [AVI-R](https://pypi.org/project/avi-r/)

### TODO

* [Decord](https://github.com/dmlc/decord)
* [MoviePy](https://pypi.org/project/moviepy/)

## API

```python
from loaders import get_loader
video_path = ...
loader_class = get_loader('AVI-R')
loader = loader_class(video_path)
for frame_batch in loader():
    # do something with the frame batch
```

## Dependency

See [actev_base](https://github.com/CMU-INF-DIVA/actev_base).

## License

See [License](LICENSE).
