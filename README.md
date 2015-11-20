# tabulator-py

[![Travis](https://img.shields.io/travis/okfn/tabulator-py.svg)](https://travis-ci.org/okfn/tabulator-py)
[![Coveralls](http://img.shields.io/coveralls/okfn/tabulator-py.svg?branch=master)](https://coveralls.io/r/okfn/tabulator-py?branch=master)

A utility library that provides a consistent interface for reading tabular data

## Usage

This section is intended to be used by end-users of the library.

### Getting Started

To get started (under development):

```
pip install tabulator
```

## Development

This section is intended to be used by tech users collaborating
on this project.

Development environment is based on `npm/gulp` as interface for developers to interact with the project.

### Getting Started

To get started activate virtual environments and install
dependencies by command:

```
source activate.sh
```

**Before pushing changes back check code style and tests**:

```
npm run check
```

### Reviewing

The project follow the next style guides:
- [Open Knowledge Coding Standards and Style Guide](https://github.com/okfn/coding-standards)
- [PEP 8 - Style Guide for Python Code](https://www.python.org/dev/peps/pep-0008/)

To check the project against Python style guide:
```
$ npm run review
```

### Testing

To run tests with coverage check:
```
$ npm run test
```
Coverage data will be in the `.coverage` file.
