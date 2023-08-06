# pyprocessors_silero_te

[![license](https://img.shields.io/github/license/oterrier/pyprocessors_silero_te)](https://github.com/oterrier/pyprocessors_silero_te/blob/master/LICENSE)
[![tests](https://github.com/oterrier/pyprocessors_silero_te/workflows/tests/badge.svg)](https://github.com/oterrier/pyprocessors_silero_te/actions?query=workflow%3Atests)
[![codecov](https://img.shields.io/codecov/c/github/oterrier/pyprocessors_silero_te)](https://codecov.io/gh/oterrier/pyprocessors_silero_te)
[![docs](https://img.shields.io/readthedocs/pyprocessors_silero_te)](https://pyprocessors_silero_te.readthedocs.io)
[![version](https://img.shields.io/pypi/v/pyprocessors_silero_te)](https://pypi.org/project/pyprocessors_silero_te/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pyprocessors_silero_te)](https://pypi.org/project/pyprocessors_silero_te/)

text repunctuation and recapitalization for 

## Installation

You can simply `pip install pyprocessors_silero_te`.

## Developing

### Pre-requesites

You will need to install `flit` (for building the package) and `tox` (for orchestrating testing and documentation building):

```
python3 -m pip install flit tox
```

Clone the repository:

```
git clone https://github.com/oterrier/pyprocessors_silero_te
```

### Running the test suite

You can run the full test suite against all supported versions of Python (3.8) with:

```
tox
```

### Building the documentation

You can build the HTML documentation with:

```
tox -e docs
```

The built documentation is available at `docs/_build/index.html.
