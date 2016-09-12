# tabulator-py

[![Travis](https://img.shields.io/travis/frictionlessdata/tabulator-py/master.svg)](https://travis-ci.org/frictionlessdata/tabulator-py)
[![Coveralls](http://img.shields.io/coveralls/frictionlessdata/tabulator-py.svg?branch=master)](https://coveralls.io/r/frictionlessdata/tabulator-py?branch=master)
[![PyPi](https://img.shields.io/pypi/v/tabulator.svg)](https://pypi.python.org/pypi/tabulator)
[![Gitter](https://img.shields.io/gitter/room/frictionlessdata/chat.svg)](https://gitter.im/frictionlessdata/chat)

Library that provides a consistent interface for reading and writing tabular data.

## Getting Started

### Installation

To get started:

```
$ pip install tabulator
```

### Quick Start

Open tabular stream from csv source:

```python
from tabulator import Stream

with Stream('path.csv', headers=1) as stream:
    for row in stream:
        print(row)  # will print row values list
```

`Stream` takes the `source` argument:

```
<scheme>://path/to/file.<format>
```
and uses corresponding `Loader` and `Parser` to open and start to iterate over the tabular stream. Also user can pass `scheme` and `format` explicitly as constructor arguments. User can force Tabulator to use encoding of choice to open the table passing `encoding` argument.

In this example we use context manager to call `stream.open()` on enter and `stream.close()` when we exit:
- stream can be iterated like file-like object returning row by row
- stream can be used for manual iterating with `iter` function
- stream can be read into memory using `read` function with row count `limit`
- headers can be accessed via `headers` property
- rows sample can be accessed via `sample` property
- stream pointer can be set to start via `reset` method
- stream could be saved to filesystem using `save` method
- `iter/read` accepts `keyed/extended` arguments to customize row output

### Advanced Usage

To get full control over the process you can use more parameters.  Below the more expanded example is presented:

```python
from tabulator import Stream

def skip_even_rows(extended_rows):
    for number, headers, row in extended_rows:
        if number % 2:
            yield (number, headers, row)

stream = Stream('source.csv',
    headers=1, encoding='utf-8', sample_size=1000,
    post_parse=[skip_even_rows], parser_options={delimeter': ',', quotechar: '|'})
stream.open()
print(stream.sample)  # will print sample
print(stream.headers)  # will print headers list
print(stream.read(limit=10))  # will print 10 rows
stream.reset()
for keyed_row in stream.iter(keyed=True):
    print keyed_row  # will print row dict
for extended_row in stream.iter(extended=True):
    print extended_row  # will print (number, headers, row) list
stream.reset()
stream.save('target.csv')
stream.close()
```

## Read more

- [Docstrings](https://github.com/frictionlessdata/tabulator-py/tree/master/tabulator)
- [Changelog](https://github.com/frictionlessdata/tabulator-py/releases)
- [Contribute](CONTRIBUTING.md)

Thanks!
