# tabulator-py

[![Travis](https://img.shields.io/travis/frictionlessdata/tabulator-py/master.svg)](https://travis-ci.org/frictionlessdata/tabulator-py)
[![Coveralls](http://img.shields.io/coveralls/frictionlessdata/tabulator-py.svg?branch=master)](https://coveralls.io/r/frictionlessdata/tabulator-py?branch=master)
[![PyPi](https://img.shields.io/pypi/v/tabulator.svg)](https://pypi.python.org/pypi/tabulator)
[![SemVer](https://img.shields.io/badge/versions-SemVer-brightgreen.svg)](http://semver.org/)
[![Gitter](https://img.shields.io/gitter/room/frictionlessdata/chat.svg)](https://gitter.im/frictionlessdata/chat)

Consistent interface for stream reading and writing tabular data (csv/xls/json/etc).

> Release `v0.10` contains changes in `exceptions` module introduced in NOT backward-compatibility manner.

## Features

- supports various formats: csv/tsv/xls/xlsx/json/ndjson/ods/gsheet/native/etc
- reads data from variables, filesystem or Internet
- streams data instead of using a lot of memory
- processes data via simple user processors
- saves data using the same interface

## Getting Started

### Installation

To get started:

```
$ pip install tabulator
```

### Example

Open tabular stream from csv source:

```python
from tabulator import Stream

with Stream('path.csv', headers=1) as stream:
    print(stream.headers) # will print headers from 1 row
    for row in stream:
        print(row)  # will print row values list
```

### Stream

`Stream` takes the `source` argument:

```
<scheme>://path/to/file.<format>
```
and uses corresponding `Loader` and `Parser` to open and start to iterate over the tabular stream. Also user can pass `scheme` and `format` explicitly as constructor arguments. User can force Tabulator to use encoding of choice to open the table passing `encoding` argument.

In this example we use context manager to call `stream.open()` on enter and `stream.close()` when we exit:
- stream can be iterated like file-like object returning row by row
- stream can be used for manual iterating with `iter(keyed/extended)` function
- stream can be read into memory using `read(keyed/extended)` function with row count `limit`
- headers can be accessed via `headers` property
- rows sample can be accessed via `sample` property
- stream pointer can be set to start via `reset` method
- stream could be saved to filesystem using `save` method

Below the more expanded example is presented:

```python
from tabulator import Stream

def skip_even_rows(extended_rows):
    for number, headers, row in extended_rows:
        if number % 2:
            yield (number, headers, row)

stream = Stream('http://example.com/source.xls',
    headers=1, encoding='utf-8', sample_size=1000,
    post_parse=[skip_even_rows], sheet=1)
stream.open()
print(stream.sample)  # will print sample
print(stream.headers)  # will print headers list
print(stream.read(limit=10))  # will print 10 rows
stream.reset()
for keyed_row in stream.iter(keyed=True):
    print keyed_row  # will print row dict
for extended_row in stream.iter(extended=True):
    print extended_row  # will print (number, headers, row)
stream.reset()
stream.save('target.csv')
stream.close()
```

For the full list of options see - https://github.com/frictionlessdata/tabulator-py/blob/master/tabulator/stream.py#L17

### CLI

> It's a provisional API excluded from SemVer. If you use it as a part of other program please pin concrete `goodtables` version to your requirements file.

The library ships with a simple CLI to read tabular data:

```bash
$ tabulator
Usage: cli.py [OPTIONS] SOURCE

Options:
  --headers INTEGER
  --scheme TEXT
  --format TEXT
  --encoding TEXT
  --limit INTEGER
  --help             Show this message and exit.
```

Shell usage example:

```bash
$ tabulator data/table.csv
id, name
1, english
2, 中国人
```

## API Reference

### Snapshot

```
Stream(source,
       headers=None,
       scheme=None,
       format=None,
       encoding=None,
       sample_size=None,
       post_parse=None,
       **options)
    closed/open/close/reset
    headers -> list
    sample -> rows
    iter(keyed/extended=False) -> (generator) (keyed/extended)row[]
    read(keyed/extended=False, limit=None) -> (keyed/extended)row[]
    save(target, format=None, encoding=None, **options)
exceptions
~cli
```

### Detailed

- [Docstrings](https://github.com/frictionlessdata/tabulator-py/tree/master/tabulator)
- [Changelog](https://github.com/frictionlessdata/tabulator-py/commits/master)

## Contributing

Please read the contribution guideline:

[How to Contribute](CONTRIBUTING.md)

Thanks!
