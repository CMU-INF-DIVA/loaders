# Loaders

Author: Lijun Yu

Email: lijun@lj-y.com

A submodule of video loaders.

## Loader List

* [AVI-R](https://pypi.org/project/avi-r/)

## API

```python
from loaders import get_loader
video_path = ...
loader_class = get_loader('AVI-R')
loader = loader_class(video_path)
for frame_batch in loader():
    # do something with the frame batch
```

## TODO

* [Decord](https://github.com/dmlc/decord)
* [MoviePy](https://pypi.org/project/moviepy/)

## License

See [License](LICENSE).
