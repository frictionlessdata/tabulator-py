# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import io
import pytest
from mock import Mock
from tabulator import parsers
from tabulator import Stream, exceptions
from tabulator.parsers.xls import XLSParser
BASE_URL = 'https://raw.githubusercontent.com/okfn/tabulator-py/master/%s'


# Stream

def test_stream_local_xls():
    with Stream('data/table.xls') as stream:
        assert stream.headers is None
        assert stream.read() == [['id', 'name'], [1.0, 'english'], [2.0, '中国人']]


def test_stream_remote_xls():
    with Stream(BASE_URL % 'data/table.xls') as stream:
        assert stream.headers is None
        assert stream.read() == [['id', 'name'], [1.0, 'english'], [2.0, '中国人']]


def test_stream_xls_sheet_by_index():
    source = 'data/special/sheet2.xls'
    with Stream(source, sheet=2) as stream:
        assert stream.read() == [['id', 'name'], [1.0, 'english'], [2.0, '中国人']]


def test_stream_xls_sheet_by_index_not_existent():
    source = 'data/special/sheet2.xls'
    with pytest.raises(exceptions.SourceError) as excinfo:
        Stream(source, sheet=3).open()
    assert 'sheet "3"' in str(excinfo.value)


def test_stream_xls_sheet_by_name():
    source = 'data/special/sheet2.xls'
    with Stream(source, sheet='Sheet2') as stream:
        assert stream.read() == [['id', 'name'], [1.0, 'english'], [2.0, '中国人']]


def test_stream_xls_sheet_by_name_not_existent():
    source = 'data/special/sheet2.xls'
    with pytest.raises(exceptions.SourceError) as excinfo:
        Stream(source, sheet='not-existent').open()
    assert 'sheet "not-existent"' in str(excinfo.value)


def test_stream_xlsx_merged_cells():
    source = 'data/special/merged-cells.xls'
    with Stream(source) as stream:
        assert stream.read() == [['data', ''], ['', ''], ['', '']]


def test_stream_xlsx_merged_cells_fill():
    source = 'data/special/merged-cells.xls'
    with Stream(source, fill_merged_cells=True) as stream:
        assert stream.read() == [['data', 'data'], ['data', 'data'], ['data', 'data']]


def test_stream_xls_with_boolean():
    with Stream('data/special/table-with-booleans.xls') as stream:
        assert stream.headers is None
        assert stream.read() == [['id', 'boolean'], [1.0, True], [2.0, False]]


def test_stream_xlsx_merged_cells_boolean():
    source = 'data/special/merged-cells-boolean.xls'
    with Stream(source) as stream:
        assert stream.read() == [[True, ''], ['', ''], ['', '']]


def test_stream_xlsx_merged_cells_fill_boolean():
    source = 'data/special/merged-cells-boolean.xls'
    with Stream(source, fill_merged_cells=True) as stream:
        assert stream.read() == [[True, True], [True, True], [True, True]]

# Parser

def test_parser_xls():

    source = 'data/table.xls'
    encoding = None
    loader = Mock()
    loader.load = Mock(return_value=io.open(source, 'rb'))
    parser = XLSParser(loader)

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
