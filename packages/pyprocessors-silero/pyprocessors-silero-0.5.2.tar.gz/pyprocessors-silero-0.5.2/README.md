# pyprocessors_silero

[![license](https://img.shields.io/github/license/oterrier/pyprocessors_silero)](https://github.com/oterrier/pyprocessors_silero/blob/master/LICENSE)
[![tests](https://github.com/oterrier/pyprocessors_silero/workflows/tests/badge.svg)](https://github.com/oterrier/pyprocessors_silero/actions?query=workflow%3Atests)
[![codecov](https://img.shields.io/codecov/c/github/oterrier/pyprocessors_silero)](https://codecov.io/gh/oterrier/pyprocessors_silero)
[![docs](https://img.shields.io/readthedocs/pyprocessors_silero)](https://pyprocessors_silero.readthedocs.io)
[![version](https://img.shields.io/pypi/v/pyprocessors_silero)](https://pypi.org/project/pyprocessors_silero/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pyprocessors_silero)](https://pypi.org/project/pyprocessors_silero/)

text repunctuation and recapitalization for 

## Installation

You can simply `pip install pyprocessors_silero`.

## Developing

### Pre-requesites

You will need to install `flit` (for building the package) and `tox` (for orchestrating testing and documentation building):

```
python3 -m pip install flit tox
```

Clone the repository:

```
git clone https://github.com/oterrier/pyprocessors_silero
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
