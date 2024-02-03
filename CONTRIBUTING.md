# Contributing to PyFilesystem3

Pull Requests are very welcome for this project!

For bug fixes or new features, please file an issue before submitting a pull
request. If the change isn't trivial, it may be best to wait for feedback.
For a quicker response, contact [Jevin Sweval (@jevinskie)](mailto:jevinsweval+pyfs3@gmail.com) directly.

## `tox`

Most of the guidelines that follow can be checked with a particular
[`tox`](https://pypi.org/project/tox/) environment. Having it installed will
help you develop and verify your code locally without having to wait for
our Continuous Integration pipeline to finish.

## Tests

New code should have unit tests. We strive to have near 100% coverage.
Get in touch, if you need assistance with the tests. You shouldn't refrain
from opening a Pull Request even if all the tests were not added yet, or if
not all of them are passing yet.

### Test Dependencies

The dependency for running the tests can be found in the `tests/requirements.txt` file.
If you're using `tox`, you won't have to install them manually. Otherwise,
they can be installed with `pip3`:

```console
$ pip3 install -r tests/requirements.txt
```

### Test Running (with `tox`)

Simply run in the repository folder to execute the tests for all available
environments:

```console
$ tox
```

Since this can take some time, you can use a single environment to run
tests only once, for instance to run tests only with Python 3.9:

```console
$ tox -e py39
```

### Test Running (without `tox`)

Tests are written using the standard [`unittest`](https://docs.python.org/3/library/unittest.html)
framework. You should be able to run them using the standard library runner:

```console
$ python3 -m unittest discover -vv
```

### Test Style

The code (including the tests) should follow PEP8. You can check for the
code style with:

```console
$ tox -e codestyle
```

This will invoke [`flake8`](https://pypi.org/project/flake8/) with some common
plugins such as [`flake8-comprehensions`](https://pypi.org/project/flake8-comprehensions/).

### Test Format

Please format new code with [black](https://github.com/ambv/black), using the
default settings. You can check whether the code is well-formatted with:

```console
$ tox -e codeformat
```

### Type Annotations

The code is typechecked with [`mypy`](https://pypi.org/project/mypy/).
Run the typechecking with:

```console
$ tox -e typecheck
```

## Documentation

### Doc Dependencies

The documentation is built with [Sphinx](https://pypi.org/project/Sphinx/),
using the [ReadTheDocs](https://pypi.org/project/sphinx-rtd-theme/) theme.
The dependencies are listed in `docs/requirements.txt` and can be installed with
`pip3`:

```console
$ pip3 install -r docs/requirements.txt
```

### Doc Building

Run the following command to build the HTML documentation:

```console
$ python3 setup.py build_sphinx
```

The documentation index will be written to the `build/sphinx/html/` directory.

### Doc Style

The API reference is written in the Python source, using docstrings in
[Google format](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html).
The documentation style can be checked with:

```console
$ tox -e docstyle
```
