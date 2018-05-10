# cmd2-submenu
This project provides a submenu system for cmd2

## Installing
To install the plugin, do:
```
$ pip install cmd2-submenu
```

## How to use

## Running tests

`cmd2` uses a three tiered testing strategy to test on multiple versions
of python on various platforms. This plugin uses the same strategy:

- [pytest](https://pytest.org) runs the unit tests
- [tox](https://tox.readthedocs.io/) runs the unit tests on multiple versions
  of python
- [AppVeyor](https://www.appveyor.com/) and [TravisCI](https://travis-ci.com)
  run the tests on the various supported platforms

### Running unit tests

Run `pytest` from the top level directory of this plugin to run all the
unit tests.

### Use tox to run unit tests in multiple versions of python

The included `tox.ini` is setup to run the unit tests in python 3.4, 3.5,
and 3.6. In order for `tox` to work, you need to have different versions of
python executables available in your path.
[pyenv](https://github.com/pyenv/pyenv) is one method of doing this easily.
Once `pyenv` is installed, use it to install multiple versions of python:

```
$ pyenv install 3.4.8
$ pyenv install 3.5.5
$ pyenv install 3.6.5
$ pyenv local 3.6.5 3.5.5 3.4.8
```

This will create a `.python-version` file and instruct the `pyenv` shims
to make `python3.6`, `python3.5`, and `python3.4` launch the appropriate
versions of python.

Once these executables are configured, invoking `tox` will create a
virtual environment for each version of python, install the prerequisite
packages, and run your unit tests.

