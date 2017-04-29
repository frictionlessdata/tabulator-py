# tabulator-py

[![Travis](https://img.shields.io/travis/frictionlessdata/tabulator-py/master.svg)](https://travis-ci.org/frictionlessdata/tabulator-py)
[![Coveralls](http://img.shields.io/coveralls/frictionlessdata/tabulator-py.svg?branch=master)](https://coveralls.io/r/frictionlessdata/tabulator-py?branch=master)
[![PyPi](https://img.shields.io/pypi/v/tabulator.svg)](https://pypi.python.org/pypi/tabulator)
[![Gitter](https://img.shields.io/gitter/room/frictionlessdata/chat.svg)](https://gitter.im/frictionlessdata/chat)

A library for reading and writing tabular data (csv/xls/json/etc).

> Version v1.0 includes deprecated API removal. Please read a [migration guide](#v10).

## Features

- supports various formats: csv/tsv/xls/xlsx/json/ndjson/ods/gsheet/native/etc
- reads data from variables, filesystem or Internet
- streams data instead of using a lot of memory
- processes data via simple user processors
- saves data using the same interface
- custom loaders, parsers and writers

## Getting started

### Installation

The package use semantic versioning. It means that major versions  could include breaking changes. It's highly recommended to specify `tabulator` version range if you use `setup.py` or `requirements.txt` file e.g. `tabulator<2.0`.

```
$ pip install tabulator --pre
```

### Examples

There are main examples and more are available in [examples](https://github.com/frictionlessdata/tabulator-py/tree/master/examples) directory.

```python
from tabulator import Stream

with Stream('path.csv', headers=1) as stream:
    print(stream.headers) # will print headers from 1 row
    for row in stream:
        print(row)  # will print row values list
```

## Documentation

The whole public API of this package is described here and follows semantic versioning rules. Everyting outside of this readme are private API and could be changed without any notification on any new version.

### Stream

The `Stream` class represents a tabular stream. It takes the `source` argument in a form of source string or object:

```
<scheme>://path/to/file.<format>
```
and uses corresponding `Loader` and `Parser` to open and start to iterate over the tabular stream. Also user can pass `scheme` and `format` explicitly as constructor arguments. User can force `tabulator` to use encoding of choice to open the table passing `encoding` argument.


```python
from tabulator import Stream

# Post parse processor
def skip_even_rows(extended_rows):
    for number, headers, row in extended_rows:
        if number % 2:
            yield (number, headers, row)

# Create stream
stream = Stream('http://example.com/source.xls',
    headers=1, encoding='utf-8', sample_size=1000,
    post_parse=[skip_even_rows], sheet=1)

# Use stream
stream.open()
stream.sample  # [[value1, value2, ...], ...]
stream.headers  # [header1, header2, ...]
stream.read(limit=10) # [[value1, value2, ...], ...]
stream.reset()
for keyed_row in stream.iter(keyed=True):
    print keyed_row  # {header1: value1, header2: value2}
for extended_row in stream.iter(extended=True):
    print extended_row  # [1, [header1, header2], [value1, value2]]
stream.reset()
stream.save('target.csv')
stream.close()
```

#### Stream(source, headers=None, scheme=None, format=None, encoding=None, sample_size=100, allow_html=False, skip_rows=[], post_parse=[], custom_loaders={}, custom_parsers={}, custom_writers={}, \*\*options)

Create stream class instance.

- **source (any)** - stream source in a form based on `scheme` argument
- **headers (list/int)** - headers list or source row number containing headers. If number is given for plain source headers row and all rows before will be removed and for keyed source no rows will be removed.
- **scheme (str)** - source scheme with `file` as default. For the most cases scheme will be inferred from source. See a list of supported schemas below.
- **format (str)** - source format with `None` (detect) as default. For the most cases format will be inferred from source.  See a list of supported formats below.
- **encoding (str)** - source encoding with  `None` (detect) as default.
- **sample_size (int)** - rows count for table.sample. Set to "0" to prevent any parsing activities before actual table.iter call. In this case headers will not be extracted from the source.
- **allow_html (bool)** - a flag to allow html
- **skip_rows (int/str[])** - list of rows to skip by row number or row comment. Example: `skip_rows=[1, 2, '#', '//']` - rows 1, 2 and all rows started with `#` and `//` will be skipped.
- **post_parse (generator[])** - post parse processors (hooks). Signature to follow is `processor(extended_rows) -> yield (row_number, headers, row)` which should yield one extended row per yield instruction.
- **custom_loaders (dict)** - loaders keyed by scheme. See a section below.
- **custom_parsers (dict)** - custom parsers keyed by format. See a section below.
- **custom_writers (dict)** - custom writers keyed by format. See a section below.
- **options (dict)** - loader/parser options. See in the scheme/format section
- returns **(Stream)** - Stream class instance

#### stream.closed

- returns **(bool)** - `True` if underlaying stream is closed

#### stream.open()

Open stream by opening underlaying stream.

#### stream.close()

Close stream by closing underlaying stream.

#### stream.reset()

Reset stream pointer to the first row.

#### stream.headers

- returns **(str[])** - data headers

#### stream.sample

- returns **(list)** - data sample

#### stream.iter()

Iter stream rows.

- **keyed (bool)** - yield keyed rows
- **extended (bool)** - yield extended rows
- returns **(any[]/any{})** - yields row/keyed row/extended row

#### stream.read(keyed=False, extended=False, limit=None)

Read table rows with count limit.

- **keyed (bool)** - return keyed rows
- **extended (bool)** - return extended rows
- **limit (int)** - rows count limit
- returns **(list)** - rows/keyed rows/extended rows

#### stream.save(target, format=None,  encoding=None, **options)

Save stream to filesystem.

- **target (str)** - stream target
- **format (str)** - saving format. See supported formats
- **encoding (str)** - saving encoding
- **options (dict)** - writer options

### Headers

TODO: write

### Schemes

#### file

It's a defaulat scheme. Source should be a file in local filesystem.

```python
stream = Stream('data.csv')
```

#### http/https/ftp/ftps

Source should be a file available via one of this protocols in the web.


```python
stream = Stream('http://example.com/data.csv')
```

#### stream

Source should be a file-like python object which supports corresponding protocol.


```python
stream = Stream(open('data.csv'))
```

#### text

Source should be a string containing tabular data. In this case `format` has to be explicitely passed because it's not possible to infer it from source string.


```python
stream = Stream('text://name,age\nJohn, 21\n', format='csv')
```

### Formats

#### csv

Source should be parsable by csv parser.

```python
stream = Stream('data.csv', delimiter=',')
```

Options:
- delimiter
- doublequote
- escapechar
- quotechar
- quoting
- skipinitialspace
- lineterminator

See options reference in [Python documentation](https://docs.python.org/3/library/csv.html#dialects-and-formatting-parameters).

#### xls/xlsx

Source should be a valid Excel document.

```python
stream = Stream('data.xls', sheet=1)
```

Options:
- sheet - sheet number starting from 1

#### gsheet

Source should be a link to publicly available Google Spreadsheet.

```python
stream = Stream('https://docs.google.com/spreadsheets/d/<id>?usp=sharing')
stream = Stream('https://docs.google.com/spreadsheets/d/<id>edit#gid=<gid>')
```

#### inline

Source should be a list of lists or a list of dicts.

```python
stream = Stream([['name', 'age'], ['John', 21], ['Alex', 33]])
stream = Stream([{'name': 'John', 'age': 21}, {'name': 'Alex', 'age': 33}])
```

#### json

Source should be a valid JSON document containing array of arrays or array of objects (see `inline` format example).

```python
stream = Stream('data.json', node='key1.key2')
```

Options:
- node - path to tabular data node separated by dots. For example having data structure like `{"response": {"data": [...]}}` you should set node to `response.data`.

#### ndjson

Source should be parsable by ndjson parser.

```python
stream = Stream('data.ndjson')
```

#### ods

Source should be a valid Open Office document.

```python
stream = Stream('data.ods', sheet=1)
```

Options:
- sheet - sheet number starting from 1

#### tsv

Source should be parsable by tsv parser.

```python
stream = Stream('data.tsv')
```

### Encoding

# TODO: write

### Sample size

# TODO: write

### Allow html

# TODO: write

### Force strings

Because `tabulator` support not only sources with string data representation as `csv` but also sources supporting different data types as `json` or `inline` there is a `Stream` option `force_strings` to stringify all data values on reading.

Here how stream works without forcing strings:

```python
with Stream([['string', 1, datetime.time(17, 00)]]) as stream:
  stream.read() # [['string', 1, datetime.time(17, 00)]]
```

The same data source using `force_strings` option:

```python
with Stream([['string', 1]], force_strings=True) as stream:
  stream.read() # [['string', '1', '17:00:00']]
```

For all temporal values stream will use ISO format. But if your data source doesn't support temporal values (for instance `json` format) `Stream` just returns it as it is without converting to ISO format.

### Skip rows

# TODO: write

### Post parse

# TODO: write

### Custom loaders

> It's a provisional API. If you use it as a part of other program please pin concrete `goodtables` version to your requirements file.

To create a custom loader `Loader` interface should be implemented and passed to `Stream` constructor as `custom_loaders={'scheme': CustomLoader}` argument.

For example let's implement a custom loader:

```python
from tabulator import Loader

class CustomLoader(Loader):
  options = []
  def load(self, source, mode='t', encofing=None, allow_zip=False):
    # load logic

with Stream(source, custom_loaders={'custom': CustomLoader}) as stream:
  stream.read()
```

#### Loader(\*\*options)

- **options (dict)** - loader options
- returns **(Loader)** - `Loader` class instance

#### loader.load(source, mode='t', encoding=None, allow_zip=False)

- **source (str)** - table source
- **mode (str)** - text stream mode: 't' or 'b'
- **encoding (str)** - encoding of source
- **allow_zip (bool)** - if false will raise on zip format
- returns **(file-like)** - file-like object of bytes or chars based on mode argument

### Custom parsers

> It's a provisional API. If you use it as a part of other program please pin concrete `goodtables` version to your requirements file.

To create a custom parser `Parser` interface should be implemented and passed to `Stream` constructor as `custom_parsers={'format': CustomParser}` argument.

For example let's implement a custom parser:

```python
from tabulator import Parser

class CustomParser(Parser):
  def __init__(self, loader):
    self.__loader = loader
  @property
  def closed(self):
    return False
  def open(self, source, encoding=None):
    # open logic
  def close(self):
    # close logic
  def reset(self):
    raise NotImplemenedError()
  @property
  def extended_rows():
    # extended rows logic

with Stream(source, custom_parsers={'custom': CustomParser}) as stream:
  stream.read()
```

#### Parser(parser, \*\*options)

Create parser class instance.

- **loader (Loader)** - loader instance
- **options (dict)** - parser options
- returns **(Parser)** - `Parser` class instance

#### parser.closed

- returns **(bool)** - `True` if parser is closed

#### parser.open(source, encoding=None)

Open underlaying stream. Parser gets byte or text stream from loader
to start emit items from this stream.

- **source (str)** - table source
- **encoding (str)** - encoding of source

#### parser.close()

Close underlaying stream.

#### parser.reset()

Reset items and underlaying stream. After reset call iterations over items will start from scratch.

#### parser.extended_rows

- returns **(iterator)** - extended rows iterator

### Custom writers

> It's a provisional API. If you use it as a part of other program please pin concrete `goodtables` version to your requirements file.

To create a custom writer `Writer` interface should be implemented and passed to `Stream` constructor as `custom_writers={'format': CustomWriter}` argument.

For example let's implement a custom writer:

```python
from tabulator import Writer

class CustomWriter(Writer):
  options = []
  def save(self, source, target, headers=None, encoding=None):
    # save logic

with Stream(source, custom_writers={'custom': CustomWriter}) as stream:
  stream.save(target)
```

#### Writer(\*\*options)

Create writer class instance.

- **options (dict)** - writer options
- returns **(Writer)** - `Writer` class instance

#### writer.save(source, target, headers=None, encoding=None)

Save source data to target.

- **source (str)** - data source
- **source (str)** - save target
- **headers (str[])** - optional headers
- **encoding (str)** - encoding of source

### Validate

For cases you don't need open the source but want to know is it supported by `tabulator` or not you could use `validate` function. It also let you know what exactly is not supported raising correspondig exception class.

```python
from tabulator import validate, exceptions

try:
  tabular = validate('data.csv')
except exceptions.TabulatorException:
  tabular = False
```

#### validate(source, scheme=None, format=None)

Validate if this source has supported scheme and format.

- **source (any)** - data source
- **scheme (str)** - data scheme
- **format (str)** - data format
- raises **(exceptions.SchemeError)** - if scheme is not supported
- raises **(exceptions.FormatError)** - if format is not supported
- returns **(bool)** - `True` if scheme/format is supported

### Exceptions

#### exceptions.TabulatorException

Base class for all `tabulator` exceptions.

#### exceptions.SourceError

This class of exceptions covers all source errors like bad data structure for JSON.

#### exceptions.SchemeError

For example this exceptions will be used if you provide not supported source scheme like `bad://source.csv`.

#### exceptions.FormatError

For example this exceptions will be used if you provide not supported source format like `http://source.bad`.

#### exceptions.EncodingError

All errors related to encoding problems.

#### exceptions.OptionsError

All errors related to not supported by Loader/Parser/Writer options.

#### exceptions.IOError

All underlaying input-output errors.

#### exceptions.HTTPError

All underlaying HTTP errors.

#### exceptions.ResetError

All errors caused by stream reset problems.

### CLI

> It's a provisional API. If you use it as a part of other program please pin concrete `goodtables` version to your requirements file.

The library ships with a simple CLI to read tabular data:

```bash
$ tabulator data/table.csv
id, name
1, english
2, 中国人
```

#### $ tabulator

```bash
Usage: cli.py [OPTIONS] SOURCE

Options:
  --headers INTEGER
  --scheme TEXT
  --format TEXT
  --encoding TEXT
  --limit INTEGER
  --help             Show this message and exit.
```

## Contributing

The project follows the [Open Knowledge International coding standards](https://github.com/okfn/coding-standards).

Recommended way to get started is to create and activate a project virtual environment.
To install package and development dependencies into active environment:

```
$ make install
```

To run tests with linting and coverage:

```bash
$ make test
```

For linting `pylama` configured in `pylama.ini` is used. On this stage it's already
installed into your environment and could be used separately with more fine-grained control
as described in documentation - https://pylama.readthedocs.io/en/latest/.

For example to sort results by error type:

```bash
$ pylama --sort <path>
```

For testing `tox` configured in `tox.ini` is used.
It's already installed into your environment and could be used separately with more fine-grained control as described in documentation - https://testrun.org/tox/latest/.

For example to check subset of tests against Python 2 environment with increased verbosity.
All positional arguments and options after `--` will be passed to `py.test`:

```bash
tox -e py27 -- -v tests/<path>
```

Under the hood `tox` uses `pytest` configured in `pytest.ini`, `coverage`
and `mock` packages. This packages are available only in tox envionments.

## Changelog

Here described only breaking and the most important changes. The full changelog could be found in nicely formatted [commit history](https://github.com/frictionlessdata/tabulator-py/commits/master).

### v1.0

This version includes deprecated API removal. A migration guide is under development and will be published here.
