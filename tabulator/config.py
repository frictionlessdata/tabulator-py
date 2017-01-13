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
    'file': 'tabulator.loaders.file.FileLoader',
    'ftp': 'tabulator.loaders.web.WebLoader',
    'ftps': 'tabulator.loaders.web.WebLoader',
    'gsheet': None,
    'http': 'tabulator.loaders.web.WebLoader',
    'https': 'tabulator.loaders.web.WebLoader',
    'native': None,
    'stream': 'tabulator.loaders.stream.StreamLoader',
    'text': 'tabulator.loaders.text.TextLoader',
}

PARSERS = {
    'csv': 'tabulator.parsers.csv.CSVParser',
    'gsheet': 'tabulator.parsers.gsheet.GsheetParser',
    'json': 'tabulator.parsers.json.JSONParser',
    'jsonl': 'tabulator.parsers.ndjson.NDJSONParser',
    'ndjson': 'tabulator.parsers.ndjson.NDJSONParser',
    'native': 'tabulator.parsers.native.NativeParser',
    'tsv': 'tabulator.parsers.tsv.TSVParser',
    'xls': 'tabulator.parsers.excel.ExcelParser',
    'xlsx': 'tabulator.parsers.excelx.ExcelxParser',
    'ods': 'tabulator.parsers.ods.ODSParser',
}

WRITERS = {
    'csv': 'tabulator.writers.csv.CSVWriter',
}
