# tabulator-py

[![Travis](https://img.shields.io/travis/frictionlessdata/tabulator-py/master.svg)](https://travis-ci.org/frictionlessdata/tabulator-py)
[![Coveralls](http://img.shields.io/coveralls/frictionlessdata/tabulator-py.svg?branch=master)](https://coveralls.io/r/frictionlessdata/tabulator-py?branch=master)
[![PyPi](https://img.shields.io/pypi/v/tabulator.svg)](https://pypi.python.org/pypi/tabulator)
[![Gitter](https://img.shields.io/gitter/room/frictionlessdata/chat.svg)](https://gitter.im/frictionlessdata/chat)

A library for reading and writing tabular data (csv/xls/json/etc).

## Features

- **Supports most common tabular formats**: CSV, XLS, ODS, JSON, Google Sheets, SQL, and others. See complete list [below](#supported-file-formats).
- **Loads local and remote data**: Supports HTTP and FTP.
- **Low memory usage**: Only the current row is kept in memory, so you can
  large datasets.
- **Supports compressed files**: Using ZIP or GZIP algorithms.
- **Extensible**: You can add support for custom file formats and loaders (e.g.
  FTP).

<!-- markdown-toc start - Don't edit this section. Run M-x markdown-toc-refresh-toc -->
## Table of Contents

- [Features](#features)
- [Getting started](#getting-started)
    - [Installation](#installation)
    - [Running on CLI](#running-on-cli)
    - [Running on Python](#running-on-python)
- [Documentation](#documentation)
    - [Stream](#stream)
        - [Options](#options)
    - [Supported schemes](#supported-schemes)
        - [file](#file)
        - [http/https/ftp/ftps](#httphttpsftpftps)
        - [stream](#stream)
        - [text](#text)
    - [Supported file formats](#supported-file-formats)
        - [csv (read & write)](#csv-read--write)
        - [xls/xlsx (read only)](#xlsxlsx-read-only)
        - [ods (read only)](#ods-read-only)
        - [gsheet (read only)](#gsheet-read-only)
        - [sql (read only)](#sql-read-only)
        - [Data Package (read only)](#data-package-read-only)
        - [inline (read only)](#inline-read-only)
        - [json (read only)](#json-read-only)
        - [ndjson (read only)](#ndjson-read-only)
        - [tsv (read only)](#tsv-read-only)
    - [Adding support for new file sources, formats, and writers](#adding-support-for-new-file-sources-formats-and-writers)
        - [Custom loaders](#custom-loaders)
        - [Custom parsers](#custom-parsers)
        - [Custom writers](#custom-writers)
    - [Validate](#validate)
    - [Exceptions](#exceptions)
- [API Reference](#api-reference)
- [Contributing](#contributing)
- [Changelog](#changelog)

<!-- markdown-toc end -->

## Getting started

### Installation

```bash
$ pip install tabulator
```

### Running on CLI

Tabulator ships with a simple CLI called `tabulator` to read tabular data. For
example:

```bash
$ tabulator https://github.com/frictionlessdata/tabulator-py/raw/4c1b3943ac98be87b551d87a777d0f7ca4904701/data/table.csv.gz
id,name
1,english
2,中国人
```

You can see all supported options by running `tabulator --help`.

### Running on Python

```python
from tabulator import Stream

with Stream('data.csv', headers=1) as stream:
    stream.headers # [header1, header2, ..]
    for row in stream:
        print(row)  # [value1, value2, ..]
```

You can find other examples in the [examples][examples-dir] directory.

## Documentation

In the following sections, we'll walk through some usage examples of
this library. All examples were tested with Python 3.6, but should
run fine with Python 3.3+.

### Stream

The `Stream` class represents a tabular stream. It takes the file path as the
`source` argument. For example:

```
<scheme>://path/to/file.<format>
```

It uses this path to determine the file format (e.g. CSV or XLS) and scheme
(e.g. HTTP or postgresql). It also supports format extraction from URLs like `http://example.com?format=csv`. If necessary, you also can define these explicitly.

Let's try it out. First, we create a `Stream` object passing the path to a CSV file.

```python
import tabulator

stream = tabulator.Stream('data.csv')
```

At this point, the file haven't been read yet. Let's open the stream so we can
read the contents.

```python
try:
    stream.open()
except tabulator.TabulatorException as e:
    pass  # Handle exception
```

This will open the underlying data stream, read a small sample to detect the
file encoding, and prepare the data to be read. We catch
`tabulator.TabulatorException` here, in case something goes wrong.

We can now read the file contents. To iterate over each row, we do:

```python
for row in stream.iter():
    print(row)  # [value1, value2, ...]
```

The `stream.iter()` method will return each row data as a list of values. If
you prefer, you could call `stream.iter(keyed=True)` instead, which returns a
dictionary with the column names as keys. Either way, this method keeps only a
single row in memory at a time. This means it can handle handle large files
without consuming too much memory.

If you want to read the entire file, use `stream.read()`. It accepts the same
arguments as `stream.iter()`, but returns all rows at once.

```python
stream.reset()
rows = stream.read()
```

Notice that we called `stream.reset()` before reading the rows. This is because
internally, tabulator only keeps a pointer to its current location in the file.
If we didn't reset this pointer, we would read starting from where we stopped.
For example, if we ran `stream.read()` again, we would get an empty list, as
the internal file pointer is at the end of the file (because we've already read
it all). Depending on the file location, it might be necessary to download the
file again to rewind (e.g. when the file was loaded from the web).

After we're done, close the stream with:

```python
stream.close()
```

The entire example looks like:

```python
import tabulator

stream = tabulator.Stream('data.csv')
try:
    stream.open()
except tabulator.TabulatorException as e:
    pass  # Handle exception

for row in stream.iter():
    print(row)  # [value1, value2, ...]

stream.reset()  # Rewind internal file pointer
rows = stream.read()

stream.close()
```

It could be rewritten to use Python's context manager interface as:

```python
import tabulator

try:
    with tabulator.Stream('data.csv') as stream:
        for row in stream.iter():
            print(row)

        stream.reset()
        rows = stream.read()
except tabulator.TabulatorException as e:
    pass
```

This is the preferred way, as Python closes the stream automatically, even if some exception was thrown along the way.

The full API documentation is available as docstrings in the [Stream source code][stream.py].

#### Options

On this section, we'll see all different options supported by the `Stream`
class.

##### Headers

By default, tabulator considers that all file rows are values (i.e. there is no
header).

```python
with Stream([['name', 'age'], ['Alex', 21]]) as stream:
  stream.headers # None
  stream.read() # [['name', 'age'], ['Alex', 21]]
```

If you have a header row, you can use the `headers` argument with the its row
number (starting from 1).

```python
# Integer
with Stream([['name', 'age'], ['Alex', 21]], headers=1) as stream:
  stream.headers # ['name', 'age']
  stream.read() # [['Alex', 21]]
```

You can also pass a lists of strings to define the headers explicitly:

```python
with Stream([['Alex', 21]], headers=['name', 'age']) as stream:
  stream.headers # ['name', 'age']
  stream.read() # [['Alex', 21]]
```

Tabulator also supports multiline headers for the `xls` and `xlsx` formats.

```python
with Stream('data.xlsx', headers=[1, 3], fill_merged_cells=True) as stream:
  stream.headers # ['header from row 1-3']
  stream.read() # [['value1', 'value2', 'value3']]
```

##### Encoding

You can specify the file encoding (e.g. `utf-8` and `latin1`) via the `encoding`
argument.

```python
with Stream(source, encoding='latin1') as stream:
  stream.read()
```

If this argument isn't set, Tabulator will try to infer it from the data. If you
get a `UnicodeDecodeError` while loading a file, try setting the encoding to
`utf-8`.

##### Compression (Python3-only)

Tabulator supports both ZIP and GZIP compression methods. By default it'll infer from the file name:

```python
with Stream('http://example.com/data.csv.zip') as stream:
  stream.read()
```

You can also set it explicitly:

```python
with Stream('data.csv.ext', compression='gz') as stream:
  stream.read()
```

##### Allow html

The `Stream` class raises `tabulator.exceptions.FormatError` if it detects HTML
contents. This helps avoiding the relatively common mistake of trying to load a
CSV file inside an HTML page, for example on GitHub.

You can disable this behaviour using the `allow_html` option:

```python
with Stream(source_with_html, allow_html=True) as stream:
  stream.read() # no exception on open
```

##### Sample size

To detect the file's headers, and run other checks like validating that the file
doesn't contain HTML, Tabulator reads a sample of rows on the `stream.open()`
method. This data is available via the `stream.sample` property. The number of
rows used can be defined via the `sample_size` parameters (defaults to 100).

```python
with Stream(two_rows_source, sample_size=1) as stream:
  stream.sample # only first row
  stream.read() # first and second rows
```

You can disable this by setting `sample_size` to zero. This way, no data will be
read on `stream.open()`.

##### Bytes sample size

Tabulator needs to read a part of the file to infer its encoding. The
`bytes_sample_size` arguments controls how many bytes will be read for this
detection (defaults to 10000).

```python
source = 'data/special/latin1.csv'
with Stream(source) as stream:
    stream.encoding # 'iso8859-2'
```

You can disable this by setting `bytes_sample_size` to zero, in which case it'll
use the machine locale's default encoding.

##### Ignore blank headers

When `True`, tabulator will ignore columns that have blank headers (defaults to
`False`).

```python
# Default behaviour
source = 'text://header1,,header3\nvalue1,value2,value3'
with Stream(source, format='csv', headers=1) as stream:
    stream.headers # ['header1', '', 'header3']
    stream.read(keyed=True) # {'header1': 'value1', '': 'value2', 'header3': 'value3'}

# Ignoring columns with blank headers
source = 'text://header1,,header3\nvalue1,value2,value3'
with Stream(source, format='csv', headers=1, ignore_blank_headers=True) as stream:
    stream.headers # ['header1', 'header3']
    stream.read(keyed=True) # {'header1': 'value1', 'header3': 'value3'}
```

##### Force strings

When `True`, all rows' values will be converted to strings (defaults to
`False`).

```python
# Default behaviour
with Stream([['string', 1, datetime.datetime(2017, 12, 1, 17, 00)]]) as stream:
  stream.read() # [['string', 1, datetime.dateime(2017, 12, 1, 17, 00)]]

# Forcing rows' values as strings
with Stream([['string', 1]], force_strings=True) as stream:
  stream.read() # [['string', '1', '2017-12-01 17:00:00']]
```

##### Force parse

When `True`, don't raise an exception when parsing a malformed row, but simply
return an empty row. Otherwise, tabulator raises
`tabulator.exceptions.SourceError` when a row can't be parsed. Defaults to `False`.

```python
# Default behaviour
with Stream([[1], 'bad', [3]]) as stream:
  stream.read() # raises tabulator.exceptions.SourceError

# With force_parse
with Stream([[1], 'bad', [3]], force_parse=True) as stream:
  stream.read() # [[1], [], [3]]
```

##### Skip rows

List of row numbers and/or strings to skip.
If it's a string, all rows that begin with it will be skipped (e.g. '#' and '//').
If it's the empty string, all rows that begin with an empty column will be skipped.

```python
source = [['John', 1], ['Alex', 2], ['#Sam', 3], ['Mike', 4], ['John', 5]]
with Stream(source, skip_rows=[1, 2, -1, '#']) as stream:
  stream.read() # [['Mike', 4]]
```

##### Post parse

List of functions that can filter or transform rows after they are parsed. These
functions receive the `extended_rows` containing the row's number, headers
list, and the row values list. They then process the rows, and yield or discard
them, modified or not.

```python
def skip_odd_rows(extended_rows):
    for row_number, headers, row in extended_rows:
        if not row_number % 2:
            yield (row_number, headers, row)

def multiply_by_two(extended_rows):
    for row_number, headers, row in extended_rows:
        doubled_row = list(map(lambda value: value * 2, row))
        yield (row_number, headers, doubled_row)

rows = [
  [1],
  [2],
  [3],
  [4],
]
with Stream(rows, post_parse=[skip_odd_rows, multiply_by_two]) as stream:
  stream.read() # [[4], [8]]
```

These functions are applied in order, as a simple data pipeline. In the example
above, `multiply_by_two` just sees the rows yielded by `skip_odd_rows`.

##### Keyed and extended rows

The methods `stream.iter()` and `stream.read()` accept the `keyed` and
`extended` flag arguments to modify how the rows are returned.

By default, every row is returned as a list of its cells values:

```python
with Stream([['name', 'age'], ['Alex', 21]]) as stream:
  stream.read() # [['Alex', 21]]
```

With `keyed=True`, the rows are returned as dictionaries, mapping the column names to their values in the row:

```python
with Stream([['name', 'age'], ['Alex', 21]]) as stream:
  stream.read(keyed=True) # [{'name': 'Alex', 'age': 21}]
```

And with `extended=True`, the rows are returned as a tuple of `(row_number,
headers, row)`, there `row_number` is the current row number (starting from 1),
`headers` is a list with the headers names, and `row` is a list with the rows
values:

```python
with Stream([['name', 'age'], ['Alex', 21]]) as stream:
  stream.read(extended=True) # (1, ['name', 'age'], ['Alex', 21])
```

### Supported schemes

#### file

The default scheme, a file in the local filesystem.

```python
stream = Stream('data.csv')
```

#### http/https/ftp/ftps

> In Python 2, `tabulator` can't stream remote data sources because of a limitation in the underlying libraries. The whole data source will be loaded to the memory. In Python 3 there is no such problem and remote files are streamed.

```python
stream = Stream('https://example.com/data.csv')
```

##### Options
- **http\_session** - a `requests.Session` object. Read more in the [requests docs][requests-session].
- **http\_stream** - Enables or disables HTTP streaming, when possible (enabled by default). Disable it if you'd like to preload the whole file into memory.

#### stream

The source is a file-like Python object.


```python
with open('data.csv') as fp:
    stream = Stream(fp)
```

#### text

The source is a string containing the tabular data. Both `scheme` and `format`
must be set explicitly, as it's not possible to infer them.

```python
stream = Stream(
    'name,age\nJohn, 21\n',
    scheme='text',
    format='csv'
)
```

### Supported file formats

In this section, we'll describe the supported file formats, and their respective
configuration options and operations. Some formats only support read operations,
while others support both reading and writing.

#### csv (read & write)

```python
stream = Stream('data.csv', delimiter=',')
```

##### Options

It supports all options from the Python CSV library. Check [their
documentation][pydoc-csv] for more information.

#### xls/xlsx (read only)

> Tabulator is unable to stream `xls` files, so the entire file is loaded in
> memory. Streaming is supported for `xlsx` files.

```python
stream = Stream('data.xls', sheet=1)
```

##### Options

- **sheet**: Sheet name or number (starting from 1)
- **fill_merged_cells**: if `True` it will unmerge and fill all merged cells by
  a visible value. With this option enabled the parser can't stream data and
  load the whole document into memory.

#### ods (read only)

> This format is not included to package by default. To use it please install `tabulator` with an `ods` extras: `$ pip install tabulator[ods]`

Source should be a valid Open Office document.

```python
stream = Stream('data.ods', sheet=1)
```

##### Options

- **sheet**: Sheet name or number (starting from 1)

#### gsheet (read only)

A publicly-accessible Google Spreadsheet.

```python
stream = Stream('https://docs.google.com/spreadsheets/d/<id>?usp=sharing')
stream = Stream('https://docs.google.com/spreadsheets/d/<id>edit#gid=<gid>')
```

#### sql (read only)

Any database URL supported by [sqlalchemy][sqlalchemy].

```python
stream = Stream('postgresql://name:pass@host:5432/database', table='data')
```

##### Options

- **table (required)**: Database table name
- **order_by**: SQL expression for row ordering (e.g. `name DESC`)

#### Data Package (read only)

> This format is not included to package by default. You can enable it by
> installing tabulator using `pip install tabulator[datapackage]`.

A [Tabular Data Package][tdp].

```python
stream = Stream('datapackage.json', resource=1)
```

##### Options

- **resource**: Resource name or index (starting from 0)

#### inline (read only)

Either a list of lists, or a list of dicts mapping the column names to their
respective values.

```python
stream = Stream([['name', 'age'], ['John', 21], ['Alex', 33]])
stream = Stream([{'name': 'John', 'age': 21}, {'name': 'Alex', 'age': 33}])
```

#### json (read only)

JSON document containing a list of lists, or a list of dicts mapping the column
names to their respective values (see the `inline` format for an example).

```python
stream = Stream('data.json', property='key1.key2')
```

##### Options

- **property**: JSON Path to the property containing the tabular data. For example, considering the JSON `{"response": {"data": [...]}}`, the `property` should be set to `response.data`.

#### ndjson (read only)

```python
stream = Stream('data.ndjson')
```

#### tsv (read only)

```python
stream = Stream('data.tsv')
```

### Adding support for new file sources, formats, and writers

Tabulator is written with extensibility in mind, allowing you to add support for
new tabular file formats, schemes (e.g. ssh), and writers (e.g. MongoDB). There
are three components that allow this:

* Loaders
  * Loads a stream from some location (e.g. ssh)
* Parsers
  * Parses a stream of tabular data in some format (e.g. xls)
* Writers
  * Writes tabular data to some destination (e.g. MongoDB)

In this section, we'll see how to write custom classes to extend any of these components.

#### Custom loaders

You can add support for a new scheme (e.g. ssh) by creating a custom loader.
Custom loaders are implemented by inheriting from the `Loader` class, and
implementing its methods. This loader can then be used by `Stream` to load data
by passing it via the `custom_loaders={'scheme': CustomLoader}` argument.

The skeleton of a custom loader looks like:

```python
from tabulator import Loader

class CustomLoader(Loader):
  options = []

  def __init__(self, bytes_sample_size, **options):
      pass

  def load(self, source, mode='t', encoding=None):
      # load logic

with Stream(source, custom_loaders={'custom': CustomLoader}) as stream:
  stream.read()
```

You can see examples of how the loaders are implemented by looking in the
`tabulator.loaders` module.

#### Custom parsers

You can add support for a new file format by creating a custom parser. Similarly
to custom loaders, custom parsers are implemented by inheriting from the
`Parser` class, and implementing its methods. This parser can then be used by
`Stream` to parse data by passing it via the `custom_parsers={'format':
CustomParser}` argument.

The skeleton of a custom parser looks like:

```python
from tabulator import Parser

class CustomParser(Parser):
    options = []

    def __init__(self, loader, force_parse, **options):
        self.__loader = loader

    def open(self, source, encoding=None):
        # open logic

    def close(self):
        # close logic

    def reset(self):
        # reset logic

    @property
    def closed(self):
        return False

    @property
    def extended_rows(self):
        # extended rows logic

with Stream(source, custom_parsers={'custom': CustomParser}) as stream:
  stream.read()
```

You can see examples of how parsers are implemented by looking in the
`tabulator.parsers` module.

#### Custom writers

You can add support to write files in a specific format by creating a custom
writer. The custom writers are implemented by inheriting from the base `Writer`
class, and implementing its methods. This writer can then be used by `Stream` to
write data via the `custom_writers={'format': CustomWriter}` argument.

The skeleton of a custom writer looks like:

```python
from tabulator import Writer

class CustomWriter(Writer):
  options = []

  def __init__(self, **options):
      pass

  def write(self, source, target, headers=None, encoding=None):
      # write logic

with Stream(source, custom_writers={'custom': CustomWriter}) as stream:
  stream.save(target)
```

You can see examples of how parsers are implemented by looking in the
`tabulator.writers` module.

### Validate

You can check if a source can be loaded by tabulator using the `validate` function.

```python
from tabulator import validate, exceptions

try:
    tabular = validate('data.csv')
except exceptions.SchemeError:
    # The file scheme isn't supported
except exceptions.FormatError:
    # The file format isn't supported
```

### Exceptions

All the exceptions thrown by tabulator inherit from
`tabulator.exceptions.TabulatorException`, so you can use it as a way to catch
any tabulator exception. You can learn about the other exceptions thrown by
looking into the [tabulator.exceptions][tabulator.exceptions] module.

## API Reference

The API reference is written as docstrings in the tabulator classes. A good
place to start is the [Stream](tabulator/stream.py) class, which manages all
loading and parsing of data files.

## Contributing

This project follows the [Open Knowledge International coding standards](https://github.com/okfn/coding-standards).

We recommend you to use `virtualenv` to isolate this project from the rest of the
packages in your machine.

To install the project and its development dependencies, run:

```bash
$ make install
```

To run the tests, use:

```bash
$ make test
```

## Changelog

Here described only breaking and the most important changes. The full changelog and documentation for all released versions could be found in nicely formatted [commit history](https://github.com/frictionlessdata/tabulator-py/commits/master).

### v1.16

New API added:
- `skip_rows` support for an empty string to skip rows with an empty first column

### v1.15

New API added:
- Format will be extracted from URLs like `http://example.com?format=csv`

### v1.14

Updated behaviour:
- Now `xls` booleans will be parsed as booleans not integers

### v1.13

New API added:
- The `skip_rows` argument now supports negative numbers to skip rows starting from the end

### v1.12

Updated behaviour:
- Instead of raising an exception, a `UserWarning` warning will be emitted if an option isn't recognized.

### v1.11

New API added:
- Added `http_session` argument for the `http/https` format (it uses `requests` now)
- Added support for multiline headers: `headers` argument accept ranges like `[1,3]`

### v1.10

New API added:
- Added support for compressed files i.e. `zip` and `gz` on Python3
- The `Stream` constructor now accepts a `compression` argument
- The `http/https` scheme now accepts a `http_stream` flag

### v1.9

Improved behaviour:
- The `headers` argument allows to set the order for keyed sources and cherry-pick values

### v1.8

New API added:
- Formats `XLS/XLSX/ODS` supports sheet names passed via the `sheet` argument
- The `Stream` constructor accepts an `ignore_blank_headers` option

### v1.7

Improved behaviour:
- Rebased `datapackage` format on `datapackage@1` library

### v1.6

New API added:
- Argument `source` for the `Stream` constructor can be a `pathlib.Path`

### v1.5

New API added:
- Argument `bytes_sample_size` for the `Stream` constructor

### v1.4

Improved behaviour:
- Updated encoding name to a canonical form

### v1.3

New API added:
- `stream.scheme`
- `stream.format`
- `stream.encoding`

Promoted provisional API to stable API:
- `Loader` (custom loaders)
- `Parser` (custom parsers)
- `Writer` (custom writers)
- `validate`

### v1.2

Improved behaviour:
- Autodetect common CSV delimiters

### v1.1

New API added:
- Added `fill_merged_cells` option to `xls/xlsx` formats

### v1.0

New API added:
- published `Loader/Parser/Writer` API
- Added `Stream` argument `force_strings`
- Added `Stream` argument `force_parse`
- Added `Stream` argument `custom_writers`

Deprecated API removal:
- removed `topen` and `Table` - use `Stream` instead
- removed `Stream` arguments `loader/parser_options` - use `**options` instead

Provisional API changed:
- Updated the `Loader/Parser/Writer` API - please use an updated version

### v0.15

Provisional API added:
- Unofficial support for `Stream` arguments `custom_loaders/parsers`


[stream.py]: tabulator/stream.py
[examples-dir]: examples "Examples"
[requests-session]: https://docs.puthon-requests.org/en/master/user/advanced/#session-objects
[pydoc-csv]: https://docs.python.org/3/library/csv.html#dialects-and-formatting-parameters "Python CSV options"
[sqlalchemy]: https://www.sqlalchemy.org/
[tdp]: https://frictionlessdata.io/specs/tabular-data-package/ "Tabular Data Package"
[tabulator.exceptions]: tabulator/exceptions.py "Tabulator Exceptions"
