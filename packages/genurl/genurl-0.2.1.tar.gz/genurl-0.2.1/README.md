# genurl

![general](https://media.giphy.com/media/JmgKSCrKZ228fIJoqt/giphy.gif)

GENerate URLs

This is a sketch of how this should work. Maybe better to use a LM than some random packages, but it is funny.

NOTE because this uses `/usr/share/dict/words` it may not work on all systems, and 100% won't work on Windows.

## Usage

```sh
$ pip install genurl
>>> installation output
$ genurl
>>> generate 1000 urls in the file urls.txt
```

You can specify `--number` of URLs to generate and the `--outfile` path.

You can also specify `--slow` if you want, to get more word diversity at the expense of going slower.

## Development

make changes, `poetry run genurl`

## Publishing

Haven't automated yet. First increment version in `pyproject.toml` and then `poetry publish --username PYPI_USERNAME --password PYPI_PASS --build`
