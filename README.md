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

### Simple interface

Fast access to the table with `topen` (stands for `table open`) function:

```python
from tabulator import topen, processors

with topen('path.csv', extract_headers=True) as table:
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
as function arguments. The last `topen` argument is `encoding` - user can force Tabulator
to use encoding of choice to open the table.

Function `topen` returns `Table` instance. We use context manager
to call `table.open()` on enter and `table.close()` when we exit:
- table can be iterated like file-like object returning row by row
- table can be read row by bow using `readrow` method (it returns row tuple)
- table can be read into memory using `read` function (return list or row tuples)
with `limit` of output rows as parameter.
- headers can be accessed via `headers` property
- table pointer can be set to start via `reset` method.

In the example above we use `processors.Headers` to extract headers
from the table (via `extract_headers=True` shortcut). Processors is a powerfull
Tabulator concept. Parsed data goes thru pipeline of processors to be updated before
returning as table row.

### Advanced interface

To get full control over the process you can use more parameters.
Below all parts of Tabulator are presented:

```python
from tabulator import topen, processors, loaders, parsers

table = topen('path.csv', encoding='utf-8',
        loader_options={'constructor': loaders.File},
        parser_options={'constructor': parsers.CSV, delimeter': ',', quotechar: '|'})
table.add_processor(processors.Headers(skip=1))
headers = table.headers
contents = table.read(limit=10)
print(headers, contents)
table.reset()
for keyed_row in table.iter(keyed=True):
    print keyed_row  # will print row dict
table.close()
```

## Design Overview

Tabulator uses modular architecture to be fully extensible and flexible.
It uses loosely coupled modules like `Loader`, `Parser` and `Processor`
to provide clear data flow.

![diagram](files/diagram.png)

## Tutorials

###How to Write a Processor

Processors is an essential Tabulator concept. Items emitted by loader-parser are processed by pipeline of processors added by user.

On every iteration every processor gets an `iterator` instance in a `process` call to modify the iteration headers or values, call skip, stop etc. A processor doesn't have to return anything:

```python
from tabulator import processors

class MyProcessor(processors.API):

    def process(self, iterator):
        # work with iterator

    def handle(self, iterator):
        # will be called on exception
```

Let's explore the iterator interface:

```
Iterator
    + skip()
    + stop()
    + index
    + count
    + keys
    + values [writable]
    + headers [writable before any data is emitted]
    + exception
```

Having this knowledge we can simply to write a processor to do the following things:

- skip any odd items
- process only 5 items
- multiply by two the second column values

```python
from tabulator import processors

class MyProcessor(processors.API):

    def process(self, iterator):
        # Skip
        if iterator.index % 2 == 0:
            iterator.skip()
        # Stop
        if iterator.index == 4:
            iterator.stop()
        # Multiply
        values = list(iterator.values)
        values[1] *= 2
        iterator.values = tuple(values)

    def handle(self, iterator):
        # will be called on exception
```

## Changelog

- 0.5.0
  - BREAKING CHANGE: updated loaders.API and parsers.API
  - BREAKING CHANGE: renamed topen argument with_headers to extract_headers
  - BREAKING CHANGE: moved topen loader_class argument to loader_options argument as constructor key
  - BREAKING CHANGE: moved topen parser_class argument to parser_options argument as constructor key
  - BREAKING CHANGE: removed topen table_class argument
  - BREAKING CHANGE: removed topen iterator_class argument
  - BREAKING CHANGE: removed topen row_class argument
  - BREAKING CHANGE: removed processors.Schema
  - BREAKING CHANGE: removed Row
  - added Table.iter(keyed=False)
  - added processors.Convert

## Contributing

Please read the contribution guideline:

[How to Contribute](CONTRIBUTING.md)

Thanks!
