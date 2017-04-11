# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import io
import pytest
from tabulator import Stream, exceptions


# Constants

BASE_URL = 'https://raw.githubusercontent.com/okfn/tabulator-py/master/%s'


# Tests [format:csv]

def test_stream_csv_excel():
    source = 'value1,value2\nvalue3,value4'
    with Stream(source, scheme='text', format='csv') as stream:
        assert stream.read() == [['value1', 'value2'], ['value3', 'value4']]


def test_stream_csv_excel_tab():
    source = 'value1\tvalue2\nvalue3\tvalue4'
    with Stream(source, scheme='text', format='csv', delimiter='\t') as stream:
        assert stream.read() == [['value1', 'value2'], ['value3', 'value4']]


def test_stream_csv_unix():
    source = '"value1","value2"\n"value3","value4"'
    with Stream(source, scheme='text', format='csv') as stream:
        assert stream.read() == [['value1', 'value2'], ['value3', 'value4']]


def test_stream_csv_escaping():
    with Stream('data/special/escaping.csv', escapechar='\\') as stream:
        assert stream.read() == [
            ['ID', 'Test'],
            ['1', 'Test line 1'],
            ['2', 'Test " line 2'],
            ['3', 'Test " line 3'],
        ]


# Tests [format:ods]

def test_stream_ods_remote():
    source = BASE_URL % 'data/table.ods'
    with Stream(source) as stream:
        assert stream.read() == [['id', 'name'], [1.0, 'english'], [2.0, '中国人']]


# Tests [format:xlsx]

def test_stream_xlsx_remote():
    source = BASE_URL % 'data/table.xlsx'
    with Stream(source) as stream:
        assert stream.read() == [['id', 'name'], [1.0, 'english'], [2.0, '中国人']]


# Tests [format:gsheet]

def test_stream_gsheet():
    source = 'https://docs.google.com/spreadsheets/d/1mHIWnDvW9cALRMq9OdNfRwjAthCUFUOACPp0Lkyl7b4/edit?usp=sharing'
    with Stream(source) as stream:
        assert stream.read() == [['id', 'name'], ['1', 'english'], ['2', '中国人']]


def test_stream_gsheet_with_gid():
    source = 'https://docs.google.com/spreadsheets/d/1mHIWnDvW9cALRMq9OdNfRwjAthCUFUOACPp0Lkyl7b4/edit#gid=960698813'
    with Stream(source) as stream:
        assert stream.read() == [['id', 'name'], ['2', '中国人'], ['3', 'german']]


def test_stream_gsheet_bad_url():
    stream = Stream('https://docs.google.com/spreadsheets/d/bad')
    with pytest.raises(exceptions.HTTPError) as excinfo:
        stream.open()


def test_stream_csv_doublequote():
    with Stream('data/special/doublequote.csv') as stream:
        for row in  stream:
            assert len(row) == 17


# Tests [format:txt]

def test_stream_txt():
    source = 'data/table.txt'
    with Stream(source) as stream:
        assert stream.read() == [['english'], ['中国人']]

def test_stream_txt_html():
    source = 'data/table.html'
    with Stream(source, format="txt") as stream:
        assert stream.read() == [['<html><table>'], ['<tr><td>english</td></tr>'], ['<tr><td>中国人</td></tr>'], ['</table></html>']]


# Tests [options]


def test_stream_skip_rows():
    source = 'data/special/skip-rows.csv'
    with Stream(source, skip_rows=['#', 4]) as stream:
        assert stream.read() == [['id', 'name'], ['1', 'english']]


def test_stream_skip_rows_with_headers():
    source = 'data/special/skip-rows.csv'
    with Stream(source, headers=2, skip_rows=['#', 1]) as stream:
        assert stream.read() == [['2', '中国人']]


# Tests [options]

def test_stream_csv_delimiter():
    source = '"value1";"value2"\n"value3";"value4"'
    with Stream(source, scheme='text', format='csv', delimiter=';') as stream:
        assert stream.read() == [['value1', 'value2'], ['value3', 'value4']]


def test_stream_csv_escapechar():
    source = 'value1%,value2\nvalue3%,value4'
    with Stream(source, scheme='text', format='csv', escapechar='%') as stream:
        assert stream.read() == [['value1,value2'], ['value3,value4']]


def test_stream_csv_quotechar():
    source = '%value1,value2%\n%value3,value4%'
    with Stream(source, scheme='text', format='csv', quotechar='%') as stream:
        assert stream.read() == [['value1,value2'], ['value3,value4']]


def test_stream_csv_quotechar():
    source = 'value1, value2\nvalue3, value4'
    with Stream(source, scheme='text', format='csv', skipinitialspace=True) as stream:
        assert stream.read() == [['value1', 'value2'], ['value3', 'value4']]


def test_stream_excel_sheet():
    source = 'data/special/sheet2.xls'
    with Stream(source, sheet=2) as stream:
        assert stream.read() == [['id', 'name'], [1.0, 'english'], [2.0, '中国人']]


def test_stream_excelx_sheet():
    source = 'data/special/sheet2.xlsx'
    with Stream(source, sheet=2) as stream:
        assert stream.read() == [['id', 'name'], [1, 'english'], [2, '中国人']]


def test_stream_json_prefix():
    source = '{"root": [["value1", "value2"], ["value3", "value4"]]}'
    with Stream(source, scheme='text', format='json', prefix='root') as stream:
        assert stream.read() == [['value1', 'value2'], ['value3', 'value4']]


# Tests [errors]

def test_stream_source_error_data():
    stream = Stream('[1,2]', scheme='text', format='json')
    with pytest.raises(exceptions.SourceError) as excinfo:
        stream.open()
        stream.read()


def test_stream_format_error_zip():
    stream = Stream('data/special/table.csv.zip', format='csv')
    with pytest.raises(exceptions.FormatError) as excinfo:
        stream.open()


def test_stream_format_error_html():
    stream = Stream('data/special/table.csv.html', format='csv')
    with pytest.raises(exceptions.FormatError) as excinfo:
        stream.open()


def test_stream_scheme_error():
    stream = Stream('', scheme='bad_scheme')
    with pytest.raises(exceptions.SchemeError) as excinfo:
        stream.open()
    assert 'bad_scheme' in str(excinfo.value)


def test_stream_format_error():
    stream = Stream('', format='bad_format')
    with pytest.raises(exceptions.FormatError) as excinfo:
        stream.open()
    assert 'bad_format' in str(excinfo.value)


def test_stream_options_error():
    with pytest.raises(exceptions.OptionsError) as excinfo:
        Stream('', scheme='text', format='csv', bad_option=True).open()
    assert 'bad_option' in str(excinfo.value)


def test_stream_io_error():
    stream = Stream('bad_path.csv')
    with pytest.raises(exceptions.IOError) as excinfo:
        stream.open()
    assert 'bad_path.csv' in str(excinfo.value)


def test_stream_http_error():
    stream = Stream('http://github.com/bad_path.csv')
    with pytest.raises(exceptions.HTTPError) as excinfo:
        stream.open()


# Tests [test]

def test_stream_test_schemes():
    # Supported
    assert Stream.test('path.csv')
    assert Stream.test('file://path.csv')
    assert Stream.test('http://example.com/path.csv')
    assert Stream.test('https://example.com/path.csv')
    assert Stream.test('ftp://example.com/path.csv')
    assert Stream.test('ftps://example.com/path.csv')
    assert Stream.test('path.csv', scheme='file')
    # Not supported
    assert not Stream.test('ssh://example.com/path.csv')
    assert not Stream.test('bad://example.com/path.csv')

def test_stream_test_formats():
    # Supported
    assert Stream.test('path.csv')
    assert Stream.test('path.json')
    assert Stream.test('path.jsonl')
    assert Stream.test('path.ndjson')
    assert Stream.test('path.tsv')
    assert Stream.test('path.xls')
    assert Stream.test('path.ods')
    assert Stream.test('path.no-format', format='csv')
    assert Stream.test('path.txt')
    # Not supported
    assert not Stream.test('path.bad')

def test_stream_test_special():
    # Gsheet
    assert Stream.test('https://docs.google.com/spreadsheets/d/id', format='csv')
    # File-like
    assert Stream.test(io.open('data/table.csv', encoding='utf-8'), format='csv')
    # Text
    assert Stream.test('text://name,value\n1,2', format='csv')
    # Native
    assert Stream.test([{'name': 'value'}])
