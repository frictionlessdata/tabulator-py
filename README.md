# tabulator-py

[![Travis](https://img.shields.io/travis/frictionlessdata/tabulator-py/master.svg)](https://travis-ci.org/frictionlessdata/tabulator-py)
[![Coveralls](http://img.shields.io/coveralls/frictionlessdata/tabulator-py.svg?branch=master)](https://coveralls.io/r/frictionlessdata/tabulator-py?branch=master)
[![PyPi](https://img.shields.io/pypi/v/tabulator.svg)](https://pypi.python.org/pypi/tabulator)
[![Gitter](https://img.shields.io/gitter/room/frictionlessdata/chat.svg)](https://gitter.im/frictionlessdata/chat)

A library for reading and writing tabular data (csv/xls/json/etc).

> Version v1.0 includes deprecated API removal and provisional API changes. Please read a [migration guide](#v10).

## Features

- supports various formats: csv/tsv/xls/xlsx/json/ndjson/ods/gsheet/inline/sql/etc
- reads data from local, remote, stream or text sources
- streams data instead of using a lot of memory
- processes data via simple user processors
- saves data using the same interface
- custom loaders, parsers and writers

## Getting started

### Installation

The package use semantic versioning. It means that major versions  could include breaking changes. It's highly recommended to specify `tabulator` version range if you use `setup.py` or `requirements.txt` file e.g. `tabulator<2.0`.

```
$ pip install tabulator # v0.15
$ pip install tabulator --pre # v1.0-alpha
```

### Examples

It's pretty simple to start with `tabulator`:

```python
from tabulator import Stream

with Stream('path.csv', headers=1) as stream:
    stream.headers # [header1, header2, ..]
    for row in stream:
        row  # [value1, value2, ..]
```

There is an [examples](https://github.com/frictionlessdata/tabulator-py/tree/master/examples) directory containing other code listings.

## Documentation

The whole public API of this package is described here and follows semantic versioning rules. Everyting outside of this readme are private API and could be changed without any notification on any new version.

### Stream

The `Stream` class represents a tabular stream. It takes the `source` argument in a form of source string or object:

```
<scheme>://path/to/file.<format>
```
and uses corresponding `Loader` and `Parser` to open and start to iterate over the tabular stream. Also user can pass `scheme` and `format` explicitly as constructor arguments. There are also alot other options described in sections below.

Let's create a simple stream object to read csv file:

```python
from tabulator import Stream

stream = Stream('data.csv')
```

This action just instantiate a stream instance. There is no actual IO interactions or source validity checks. We need to open the stream object.

```python
stream.open()
```

This call will validate data source, open underlaying stream and read the data sample (if it's not disabled). All possible exceptions will be raised on `stream.open` call not on constructor call.

After work with the stream is done it could be closed:

```python
stream.close()
```

The `Stream` class supports Python context manager interface so calls above could be written using `with` syntax. It's a common and recommended way to use `tabulator` stream:

```pytnon
with Stream('data.csv') as stream:
  # use stream
```

Now we could iterate over rows in our tabular data source. It's important to understand that `tabulator` uses underlaying streams not loading it to memory (just one row at time). So the `stream.iter()` interface is the most effective way to use the stream:

```python
for row in stream.iter():
  row # [value1, value2, ..]
```

But if you need all the data in one call you could use `stream.read()` function instead of `stream.iter()` function. But if you just run it after code snippet above the `stream.read()` call will return an empty list. That another important following of stream nature of `tabulator` - the `Stream` instance just iterates over an underlaying stream. The underlaying stream has internal pointer (for example as file-like object has). So after we've iterated over all rows in the first listing the pointer is set to the end of stream.

```python
stream.read() # []
```

The recommended way is to iterate (or read) over stream just once (and save data to memory if needed). But there is a possibility to reset the steram pointer. For some sources it will not be effective (another HTTP request for remote source). But if you work with local file as a source for example it's just a cheap `file.seek()` call:

```
stream.reset()
stream.read() # [[value1, value2, ..], ..]
```

The `Stream` class supports saving tabular data stream to the filesystem. Let's reset stream again (dont' forget about the pointer) and save it to the disk:

```
stream.reset()
stream.save('data-copy.csv')
```

The full session will be looking like this:

```python
from tabulator import Stream

with Stream('data.csv') as stream:
  for row in stream.iter():
    row # [value1, value2, ..]
  stream.reset()
  stream.read() # [[value1, value2, ..], ..]
  stream.reset()
  stream.save('data-copy.csv')
```

It's just a pretty basic `Stream` introduction. Please read the full documentation below and about `Stream` arguments in more detail in following sections. There are many other goodies like headers extraction, keyed output, post parse processors and many more!

#### Stream(source, headers=None, scheme=None, format=None, encoding=None, sample_size=100, allow_html=False, skip_rows=[], post_parse=[], custom_loaders={}, custom_parsers={}, custom_writers={}, \*\*options)

Create stream class instance.

- **source (any)** - stream source in a form based on `scheme` argument
- **headers (list/int)** - headers list or source row number containing headers. If number is given for plain source headers row and all rows before will be removed and for keyed source no rows will be removed.
- **scheme (str)** - source scheme with `file` as default. For the most cases scheme will be inferred from source. See a list of supported schemas below.
- **format (str)** - source format with `None` (detect) as default. For the most cases format will be inferred from source.  See a list of supported formats below.
- **encoding (str)** - source encoding with  `None` (detect) as default.
- **sample_size (int)** - rows count for table.sample. Set to "0" to prevent any parsing activities before actual table.iter call. In this case headers will not be extracted from the source.
- **allow_html (bool)** - a flag to allow html
- **force_strings (bool)** - if `True` all output will be converted to strings
- **force_parse (bool)** - if `True` on row parsing error a stream will return an empty row instead of raising an exception
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

#### stream.iter(keyed=False, extended=False)

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

By default `Stream` considers all data source rows as values:

```python
with Stream([['name', 'age'], ['Alex', 21]]):
  stream.headers # None
  stream.read() # [['name', 'age'], ['Alex', 21]]
```

To alter this behaviour `headers` argument is supported by `Stream` constructor. This argument could be an integer - row number starting from 1 containing headers:

```python
# Integer
with Stream([['name', 'age'], ['Alex', 21]], headers=1):
  stream.headers # ['name', 'age']
  stream.read() # [['Alex', 21]]
```

Or it could be a list of strings - user-defined headers:

```python
with Stream([['Alex', 21]], headers=['name', 'age']):
  stream.headers # ['name', 'age']
  stream.read() # [['Alex', 21]]
```

If `headers` is a row number and data source is not keyed all rows before this row and this row will be removed from data stream (see first example).

### Schemes

There is a list of all supported schemes.

#### file

It's a defaulat scheme. Source should be a file in local filesystem.

```python
stream = Stream('data.csv')
```

#### http/https/ftp/ftps

> In Python 2 `tabulator` can't stream remote data source because of underlaying libraries limitation. The whole data source will be loaded to the memory. In Python 3 there is no such a problem and `tabulator` is able to stream remote data source as expected.

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

There is a list of all supported formats. Formats support `read` operation could be opened by `Stream.open()` and formats support `write` operation could be used in `Stream.save()`.

#### csv

Source should be parsable by csv parser.

```python
stream = Stream('data.csv', delimiter=',')
```

Operations:
- read
- write

Options:
- delimiter
- doublequote
- escapechar
- quotechar
- quoting
- skipinitialspace
- lineterminator

See options reference in [Python documentation](https://docs.python.org/3/library/csv.html#dialects-and-formatting-parameters).

#### datapackage

> This format is not included to package by default. To use it please install `tabulator` with an `datapackage` extras: `$ pip install tabulator[datapackage]`

Source should be a valid Tabular Data Package see (https://frictionlessdata.io).

```python
stream = Stream('datapackage.json', resource=1)
```

Operations:
- read

Options:
- resource - resource index (starting from 0) or resource name

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

Operations:
- read

#### json

Source should be a valid JSON document containing array of arrays or array of objects (see `inline` format example).

```python
stream = Stream('data.json', property='key1.key2')
```

Operations:
- read

Options:
- property - path to tabular data property separated by dots. For example having data structure like `{"response": {"data": [...]}}` you should set property to `response.data`.

#### ndjson

Source should be parsable by ndjson parser.

```python
stream = Stream('data.ndjson')
```

Operations:
- read

#### ods

> This format is not included to package by default. To use it please install `tabulator` with an `ods` extras: `$ pip install tabulator[ods]`

Source should be a valid Open Office document.

```python
stream = Stream('data.ods', sheet=1)
```

Operations:
- read

Options:
- sheet - sheet number starting from 1

#### sql

Source should be a valid database URL supported by `sqlalchemy`.

```python
stream = Stream('postgresql://name:pass@host:5432/database', table='data')
```

Operations:
- read

Options:
- table - database table name to read data (REQUIRED)
- order_by - SQL expression to order rows e.g. `name desc`

#### tsv

Source should be parsable by tsv parser.

```python
stream = Stream('data.tsv')
```

Operations:
- read

#### xls/xlsx

> For `xls` format `tabulator` can't stream data source because of underlaying libraries limitation. The whole data source will be loaded to the memory. For `xlsx` format there is no such a problem and `tabulator` is able to stream data source as expected.

Source should be a valid Excel document.

```python
stream = Stream('data.xls', sheet=1)
```

Operations:
- read

Options:
- sheet - sheet number starting from 1
- fill_merged_cells - if `True` it will unmerge and fill all merged cells by a visible value. With this option enabled the parser can't stream data and load the whole document into memory.

### Encoding

`Stream` constructor accepts `encoding` argument to ensure needed encoding will be used. As a value argument supported by python encoding name could be used:

```python
with Stream(source, encoding='latin1') as stream:
  stream.read()
```

By default an encoding will be detected automatically.


### Sample size

By default `Stream` will read some data on `stream.open()` call in advance. This data is provided as `stream.sample`. The size of this sample could be set in rows using `sample_size` argument of stream constructor:

```python
with Stream(two_rows_source, sample_size=1) as stream:
  stream.sample # only first row
  stream.read() # first and second rows
```

Data sample could be really useful if you want to implement some initial data checks without moving stream pointer as `stream.iter/read` do. But if you don't want any interactions with an actual source before first `stream.iter/read` call just disable data smapling with `sample_size=0`.

### Allow html

By default `Stream` will raise `exceptions.FormatError` on `stream.open()` call if html contents is detected. It's not a tabular format and for example providing link to csv file inside html (e.g. GitHub page) is a common mistake.

But sometimes this default behaviour is not what is needed. For example you write custom parser which should support html contents. In this case `allow_html` option for `Stream` could be used:

```python
with Stream(sorce_with_html, allow_html=True) as stream:
  stream.read() # no exception on open
```

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

### Force parse

Some data source could be partially mailformed for a parser. For example `inline` source could have good rows (lists or dicts) and bad rows (for example strings). By default `stream.iter/read` will raise `exceptions.SourceError` on the first bad row:

```python
with Stream([[1], 'bad', [3]]) as stream:
  stream.read() # raise exceptions.SourceError
```

With `force_parse` option for `Stream` constructor this default behaviour could be changed.
If it's set to `True` non-parsable rows will be returned as empty rows:

```python
with Stream([[1], 'bad', [3]]) as stream:
  stream.read() # [[1], [], [3]]
```

### Skip rows

It's a very common situation when your tabular data contains some rows you want to skip. It could be blank rows or commented rows. `Stream` constructors accepts `skip_rows` argument to make it possible. Value of this argument should be a list of integers and strings where:
- integer is a row number starting from 1
- string is a first row chars indicating that row is a comment

Let's skip first, second and commented by '#' symbol rows:

```python
source = [['John', 1], ['Alex', 2], ['#Sam', 3], ['Mike', 4]]
with Stream(source, skip_rows=[1, 2, '#']) as stream
  stream.read() # [['Mike', 4]]
```

### Post parse

Skipping rows is a very basic ETL (extrac-transform-load) feature. For more advanced data transormations there are post parse processors.

```python
def skip_odd_rows(extended_rows):
    for row_number, headers, row in extended_rows:
        if not row_number % 2:
            yield (row_number, headers, row)

def multiply_on_two(extended_rows):
    for row_number, headers, row in extended_rows:
        yield (row_number, headers, list(map(lambda value: value * 2, row)))


with Stream([[1], [2], [3], [4]], post_parse=[skip_odd_rows, multiply_on_two]) as stream:
  stream.read() # [[4], [8]]
```

Post parse processor gets extended rows (`[row_number, headers, row]`) iterator and must yields updated extended rows back. This interface is very powerful because every processors have full control on iteration process could skip rows, catch exceptions etc.

Processors will be applied to source from left to right. For example in listing above `multiply_on_two` processor gets rows from `skip_odd_rows` processor.

### Custom loaders

> It's a provisional API. If you use it as a part of other program please pin concrete `goodtables` version to your requirements file.

To create a custom loader `Loader` interface should be implemented and passed to `Stream` constructor as `custom_loaders={'scheme': CustomLoader}` argument.

For example let's implement a custom loader:

```python
from tabulator import Loader

class CustomLoader(Loader):
  options = []
  def load(self, source, mode='t', encoding=None, allow_zip=False):
    # load logic

with Stream(source, custom_loaders={'custom': CustomLoader}) as stream:
  stream.read()
```

There are more examples in internal `tabulator.loaders` module.

#### Loader(\*\*options)

- **options (dict)** - loader options
- returns **(Loader)** - `Loader` class instance

#### Loader.options

List of supported options.

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

There are more examples in internal `tabulator.parsers` module.

#### Parser(loader, \*\*options)

Create parser class instance.

- **loader (Loader)** - loader instance
- **options (dict)** - parser options
- returns **(Parser)** - `Parser` class instance

#### Parser.options

List of supported options.

#### parser.closed

- returns **(bool)** - `True` if parser is closed

#### parser.open(source, encoding=None, force_parse=False)

Open underlaying stream. Parser gets byte or text stream from loader
to start emit items from this stream.

- **source (str)** - table source
- **encoding (str)** - encoding of source
- **force_parse (bool)** - if True parser must yield (row_number, None, []) if there is an row in parsing error instead of stopping the iteration by raising an exception

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

There are more examples in internal `tabulator.writers` module.

#### Writer(\*\*options)

Create writer class instance.

- **options (dict)** - writer options
- returns **(Writer)** - `Writer` class instance

#### Writer.options

List of supported options.

#### writer.save(source, target, headers=None, encoding=None)

Save source data to target.

- **source (str)** - data source
- **source (str)** - save target
- **headers (str[])** - optional headers
- **encoding (str)** - encoding of source

### Keyed and extended rows

Stream methods `stream.iter/read()` accept `keyed` and `extended` flags to vary data structure of output data row.

By default a stream returns every row as a list:

```python
with Stream([['name', 'age'], ['Alex', 21]]) as stream:
  stream.read() # [['Alex', 21]]
```

With `keyed=True` a stream returns every row as a dict:

```python
with Stream([['name', 'age'], ['Alex', 21]]) as stream:
  stream.read(keyed=True) # [{'name': 'Alex', 'age': 21}]
```

And with `extended=True` a stream returns every row as a tuple contining row number starting from 1, headers as a list and row as a list:

```python
with Stream([['name', 'age'], ['Alex', 21]]) as stream:
  stream.read(extended=True) # (1, ['name', 'age'], ['Alex', 21])
```

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

#### exceptions.IOError

All underlaying input-output errors.

#### exceptions.HTTPError

All underlaying HTTP errors.

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

New API added:
- published `Loader/Parser/Writer` API
- added `Stream` argument `force_strings`
- added `Stream` argument `force_parse`
- added `Stream` argument `custom_writers`

Deprecated API removal:
- removed `topen` and `Table` - use `Stream` instead
- removed `Stream` arguments `loader/parser_options` - use `**options` instead

Provisional API changed:
- updated `Loader/Parser/Writer` API - please use an updated version

### [v0.15](https://github.com/frictionlessdata/tabulator-py/tree/v0.15.0)

Provisional API added:
- unofficial support for `Stream` arguments `custom_loaders/parsers`
