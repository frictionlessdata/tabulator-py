# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import io
import pytest
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


def test_stream_xlsx_sheet_by_index():
    source = 'data/special/sheet2.xlsx'
    with Stream(source, sheet=2) as stream:
        assert stream.fragment == 'Sheet2'
        assert stream.read() == [['id', 'name'], [1, 'english'], [2, '中国人']]


def test_stream_xlsx_sheet_by_index_not_existent():
    source = 'data/special/sheet2.xlsx'
    with pytest.raises(exceptions.SourceError) as excinfo:
        Stream(source, sheet=3).open()
    assert 'sheet "3"' in str(excinfo.value)


def test_stream_xlsx_sheet_by_name():
    source = 'data/special/sheet2.xlsx'
    with Stream(source, sheet='Sheet2') as stream:
        assert stream.fragment == 'Sheet2'
        assert stream.read() == [['id', 'name'], [1, 'english'], [2, '中国人']]


def test_stream_xlsx_sheet_by_name_not_existent():
    source = 'data/special/sheet2.xlsx'
    with pytest.raises(exceptions.SourceError) as excinfo:
        Stream(source, sheet='not-existent').open()
    assert 'sheet "not-existent"' in str(excinfo.value)


def test_stream_xlsx_merged_cells():
    source = 'data/special/merged-cells.xlsx'
    with Stream(source) as stream:
        assert stream.read() == [['data', None]]


def test_stream_xlsx_merged_cells_fill():
    source = 'data/special/merged-cells.xlsx'
    with Stream(source, fill_merged_cells=True) as stream:
        assert stream.read() == [['data', 'data'], ['data', 'data'], ['data', 'data']]


def test_stream_xlsx_adjust_floating_point_error():
    source = 'data/special/adjust_floating_point_error.xlsx'
    with Stream(
        source,
        headers=1,
        ignore_blank_headers=True,
        preserve_formatting=True,
    ) as stream:
        assert stream.read(keyed=True)[1]['actual PO4 (values)'] == 274.65999999999997
    with Stream(
        source,
        headers=1,
        ignore_blank_headers=True,
        preserve_formatting=True,
        adjust_floating_point_error=True,
    ) as stream:
        assert stream.read(keyed=True)[1]['actual PO4 (values)'] == 274.66


def test_stream_xlsx_preserve_formatting():
    source = 'data/special/preserve-formatting.xlsx'
    with Stream(source, headers=1,
            ignore_blank_headers=True, preserve_formatting=True) as stream:
        assert stream.read(keyed=True) == [{

            # general
            'empty': None,

            # numeric
            '0': '1001',
            '0.00': '1000.56',
            '0.0000': '1000.5577',
            '0.00000': '1000.55770',
            '0.0000#': '1000.5577',

            # temporal
            'm/d/yy': '5/20/40',
            'd-mmm': '20-May',
            'mm/dd/yy': '05/20/40',
            'mmddyy': '052040',
            'mmddyyam/pmdd': '052040AM20',

        }]


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
