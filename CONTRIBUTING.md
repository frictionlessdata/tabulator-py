# Contributing

The contributing guideline.

## Getting Started

Recommended way to get started is to create and activate a project virtual environment. 
To install package and development dependencies into active environment:

```
$ make develop
```

## Linting

The project follow the next style guides:
- [Open Knowledge Coding Standards and Style Guide](https://github.com/okfn/coding-standards)
- [PEP 8 - Style Guide for Python Code](https://www.python.org/dev/peps/pep-0008/)

To check the project against Python style guide:

```
$ make lint
```

Under the hood `pylint` configured in `.pylintrc` is used. On this stage it's already 
installed into your environment and could be used separarely with more fine-grained control 
as described in documentation - https://www.pylint.org/.

For example to check only errors:

```
$ pylint -E <path> 
```

## Testing

To run tests with coverage:

```
$ make test
```
Under the hood `tox` powered by `py.test` and `coverage` configured in `tox.ini` is used. 
It's already installed into your environment and could be used separarely with more fine-grained control 
as described in documentation - https://testrun.org/tox/latest/.

For example to check subset of tests against Python 2 environment with increased verbosity:

```
tox -e py27 tests/<path> -- -v
```
