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
LOADERS = {
    'file': 'tabulator.loaders.local.LocalLoader',
    'ftp': 'tabulator.loaders.remote.RemoteLoader',
    'ftps': 'tabulator.loaders.remote.RemoteLoader',
    'http': 'tabulator.loaders.remote.RemoteLoader',
    'https': 'tabulator.loaders.remote.RemoteLoader',
    'stream': 'tabulator.loaders.stream.StreamLoader',
    'text': 'tabulator.loaders.text.TextLoader',
}

PARSERS = {
    'csv': 'tabulator.parsers.csv.CSVParser',
    'gsheet': 'tabulator.parsers.gsheet.GsheetParser',
    'json': 'tabulator.parsers.json.JSONParser',
    'jsonl': 'tabulator.parsers.ndjson.NDJSONParser',
    'ndjson': 'tabulator.parsers.ndjson.NDJSONParser',
    'inline': 'tabulator.parsers.inline.InlineParser',
    'tsv': 'tabulator.parsers.tsv.TSVParser',
    'xls': 'tabulator.parsers.excel.ExcelParser',
    'xlsx': 'tabulator.parsers.excelx.ExcelxParser',
    'ods': 'tabulator.parsers.ods.ODSParser',
}

WRITERS = {
    'csv': 'tabulator.writers.csv.CSVWriter',
}
