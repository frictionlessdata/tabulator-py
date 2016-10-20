# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals


# Module API

DEFAULT_SCHEME = 'file'
DEFAULT_ENCODING = 'utf-8'
ENCODING_DETECTION_MAX_LINES = 1000
ENCODING_DETECTION_MIN_CONFIDENCE = 0.5
LOADERS = {
    'file': 'tabulator.loaders.file.FileLoader',
    'ftp': 'tabulator.loaders.web.WebLoader',
    'ftps': 'tabulator.loaders.web.WebLoader',
    'http': 'tabulator.loaders.web.WebLoader',
    'https': 'tabulator.loaders.web.WebLoader',
    'native': 'tabulator.loaders.native.NativeLoader',
    'stream': 'tabulator.loaders.stream.StreamLoader',
    'text': 'tabulator.loaders.text.TextLoader',
}

PARSERS = {
    'csv': 'tabulator.parsers.csv.CSVParser',
    'json': 'tabulator.parsers.json.JSONParser',
    'native': 'tabulator.parsers.native.NativeParser',
    'tsv': 'tabulator.parsers.tsv.TSVParser',
    'xls': 'tabulator.parsers.excel.ExcelParser',
    'xlsx': 'tabulator.parsers.excelx.ExcelxParser',
}

WRITERS = {
    'csv': 'tabulator.writers.csv.CSVWriter',
}
