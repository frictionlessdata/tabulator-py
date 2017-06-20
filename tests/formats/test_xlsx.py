# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import io
from mock import Mock
from tabulator import Stream, exceptions
from tabulator.parsers.xlsx import XLSXParser
BASE_URL = 'https://raw.githubusercontent.com/okfn/tabulator-py/master/%s'


# Stream

def test_stream_xlsx_remote():
    source = BASE_URL % 'data/table.xlsx'
    with Stream(source) as stream:
        assert stream.read() == [['id', 'name'], [1.0, 'english'], [2.0, '中国人']]


def test_stream_xlsx_stream():
    source = io.open('data/table.xlsx', mode='rb')
    with Stream(source, format='xlsx') as stream:
        assert stream.headers is None
        assert stream.read() == [['id', 'name'], [1.0, 'english'], [2.0, '中国人']]


def test_stream_xlsx_sheet():
    source = 'data/special/sheet2.xlsx'
    with Stream(source, sheet=2) as stream:
        assert stream.read() == [['id', 'name'], [1, 'english'], [2, '中国人']]


def test_stream_xlsx_merged_cells():
    source = 'data/special/merged-cells.xlsx'
    with Stream(source) as stream:
        assert stream.read() == [['data', None]]


def test_stream_xlsx_merged_cells_fill():
    source = 'data/special/merged-cells.xlsx'
    with Stream(source, fill_merged_cells=True) as stream:
        assert stream.read() == [['data', 'data'], ['data', 'data'], ['data', 'data']]


# Parser

def test_parser_xlsx():

    source = 'data/table.xlsx'
    encoding = None
    loader = Mock()
    loader.load = Mock(return_value=io.open(source, 'rb'))
    parser = XLSXParser(loader)

    assert parser.closed
    parser.open(source, encoding=encoding)
    assert not parser.closed

    assert list(parser.extended_rows) == [
        (1, None, ['id', 'name']),
        (2, None, [1.0, 'english']),
        (3, None, [2.0, '中国人'])]

    assert len(list(parser.extended_rows)) == 0
    parser.reset()
    assert len(list(parser.extended_rows)) == 3

    parser.close()
    assert parser.closed
