# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals


# General

DEFAULT_SCHEME = 'file'
DEFAULT_ENCODING = 'utf-8'
BYTES_SAMPLE_SIZE = 1000
ENCODING_CONFIDENCE = 0.5
CSV_SAMPLE_LINES = 100
# http://docs.sqlalchemy.org/en/latest/dialects/index.html
SQL_SCHEMES = ['firebird', 'mssql', 'mysql', 'oracle', 'postgresql', 'sqlite', 'sybase']

# Loaders

LOADERS = {
    'file': 'tabulator.loaders.local.LocalLoader',
    'http': 'tabulator.loaders.remote.RemoteLoader',
    'https': 'tabulator.loaders.remote.RemoteLoader',
    'ftp': 'tabulator.loaders.remote.RemoteLoader',
    'ftps': 'tabulator.loaders.remote.RemoteLoader',
    'stream': 'tabulator.loaders.stream.StreamLoader',
    'text': 'tabulator.loaders.text.TextLoader',
}

# Parsers

PARSERS = {
    'csv': 'tabulator.parsers.csv.CSVParser',
    'datapackage': 'tabulator.parsers.datapackage.DataPackageParser',
    'gsheet': 'tabulator.parsers.gsheet.GsheetParser',
    'inline': 'tabulator.parsers.inline.InlineParser',
    'json': 'tabulator.parsers.json.JSONParser',
    'jsonl': 'tabulator.parsers.ndjson.NDJSONParser',
    'ndjson': 'tabulator.parsers.ndjson.NDJSONParser',
    'ods': 'tabulator.parsers.ods.ODSParser',
    'sql': 'tabulator.parsers.sql.SQLParser',
    'tsv': 'tabulator.parsers.tsv.TSVParser',
    'xls': 'tabulator.parsers.xls.XLSParser',
    'xlsx': 'tabulator.parsers.xlsx.XLSXParser',
}

# Writers

WRITERS = {
    'csv': 'tabulator.writers.csv.CSVWriter',
}
