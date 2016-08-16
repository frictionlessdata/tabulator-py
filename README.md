# tabulator-py

[![Travis](https://img.shields.io/travis/frictionlessdata/tabulator-py/master.svg)](https://travis-ci.org/frictionlessdata/tabulator-py)
[![Coveralls](http://img.shields.io/coveralls/frictionlessdata/tabulator-py.svg?branch=master)](https://coveralls.io/r/frictionlessdata/tabulator-py?branch=master)
[![PyPi](https://img.shields.io/pypi/v/tabulator.svg)](https://pypi.python.org/pypi/tabulator)
[![Gitter](https://img.shields.io/gitter/room/frictionlessdata/chat.svg)](https://gitter.im/frictionlessdata/chat)

A utility library that provides a consistent interface for reading tabular data.

## Getting Started

### Installation

To get started (under development):

```
$ pip install tabulator
```

### Quick Start

Fast access to the table with `topen` (stands for `table open`) function:

```python
from tabulator import topen, processors

with topen('path.csv', headers='row1') as table:
    for row in table:
        print(row)  # will print row tuple
```

For the most use cases `topen` function is enough. It takes the
`source` argument:

```
<scheme>://path/to/file.<format>
```
and uses corresponding `Loader` and `Parser` to open and start to iterate
over the table. Also user can pass `scheme` and `format` explicitly
as function arguments. User can force Tabulator to use encoding of choice
to open the table passing `encoding` argument.

Function `topen` returns `Table` instance. We use context manager
to call `table.open()` on enter and `table.close()` when we exit:
- table can be iterated like file-like object returning row by row
- table can be used for manual iterating with `table.iter(keye/extended=False)`
- table can be read into memory using `read` function (return list or row tuples)
with `limit` of output rows as parameter.
- headers can be accessed via `headers` property
- rows sample can be accessed via `samle` property
- table pointer can be set to start via `reset` method.

### Advanced Usage

To get full control over the process you can use more parameters.
Below the more expanded example is presented:

```python
from tabulator import topen, loaders, parsers, processors

def skip_odd_rows(extended_rows):
    for number, headers, row in extended_rows:
        if number % 2:
            yield (number, headers, row)

table = topen('path.csv', headers='row1', encoding='utf-8', sample_size=1000,
        post_parse=[processors.skip_blank_rows, skip_odd_rows]
        loader_options={'constructor': loaders.File},
        parser_options={'constructor': parsers.CSV, delimeter': ',', quotechar: '|'})
print(table.samle)  # will print sample
print(table.headers)  # will print headers list
print(table.read(limit=10))  # will print 10 rows
table.reset()
for keyed_row in table.iter(keyed=True):
    print keyed_row  # will print row dict
for extended_row in table.iter(extended=True):
    print extended_row  # will print (number, headers, row) list
table.close()
```

## Read more

- [Documentation](https://github.com/frictionlessdata/tabulator-py/tree/master/tabulator)
- [Changelog](https://github.com/frictionlessdata/tabulator-py/releases)
- [Contribute](CONTRIBUTING.md)

Thanks!
