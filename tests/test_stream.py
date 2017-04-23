# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import io
import pytest
from tabulator import Stream, exceptions
from tabulator.loaders.local import LocalLoader
from tabulator.parsers.csv import CSVParser
from tabulator.writers.csv import CSVWriter


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


# Tests [allow html]

def test_html_content():
    # Link to html file containing information about csv file
    source = 'https://github.com/frictionlessdata/tabulator-py/blob/master/data/table.csv'
    with pytest.raises(exceptions.FormatError) as excinfo:
        Stream(source).open()
    assert 'HTML' in str(excinfo.value)


def test_html_content_with_allow_html():
    # Link to html file containing information about csv file
    source = 'https://github.com/frictionlessdata/tabulator-py/blob/master/data/table.csv'
    with Stream(source, allow_html=True) as stream:
        assert stream


# Tests [skip rows]


def test_stream_skip_rows():
    source = 'data/special/skip-rows.csv'
    with Stream(source, skip_rows=['#', 4]) as stream:
        assert stream.read() == [['id', 'name'], ['1', 'english']]


def test_stream_skip_rows_with_headers():
    source = 'data/special/skip-rows.csv'
    with Stream(source, headers=2, skip_rows=['#', 1]) as stream:
        assert stream.read() == [['2', '中国人']]


# Tests [custom loaders]


def test_custom_loaders():
    source = 'custom://data/table.csv'
    class CustomLoader(LocalLoader):
        def load(self, source, *args, **kwargs):
            return super(CustomLoader, self).load(
                source.replace('custom://', ''), *args, **kwargs)
    with Stream(source, custom_loaders={'custom': CustomLoader}) as stream:
        assert stream.read() == [['id', 'name'], ['1', 'english'], ['2', '中国人']]


# Tests [custom parsers]


def test_custom_parsers():
    source = 'data/table.custom'
    class CustomParser(CSVParser):
        def open(self, source, *args, **kwargs):
            return super(CustomParser, self).open(
                source.replace('custom', 'csv'), *args, **kwargs)
    with Stream(source, custom_parsers={'custom': CustomParser}) as stream:
        assert stream.read() == [['id', 'name'], ['1', 'english'], ['2', '中国人']]


# Tests [custom writers]

def test_save_custom_writers(tmpdir):
    source = 'data/table.csv'
    target = str(tmpdir.join('table.csv'))
    class CustomWriter(CSVWriter): pass
    with Stream(source, headers=1, custom_writers={'csv': CustomWriter}) as stream:
        stream.save(target)
    with Stream(target, headers=1) as stream:
        assert stream.headers == ['id', 'name']
        assert stream.read(extended=True) == [
            (2, ['id', 'name'], ['1', 'english']),
            (3, ['id', 'name'], ['2', '中国人'])]


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


# Tests [save]

def test_save_csv(tmpdir):
    source = 'data/table.csv'
    target = str(tmpdir.join('table.csv'))
    with Stream(source, headers=1) as stream:
        stream.save(target)
    with Stream(target, headers=1) as stream:
        assert stream.headers == ['id', 'name']
        assert stream.read(extended=True) == [
            (2, ['id', 'name'], ['1', 'english']),
            (3, ['id', 'name'], ['2', '中国人'])]


def test_save_xls(tmpdir):
    source = 'data/table.csv'
    target = str(tmpdir.join('table.xls'))
    with Stream(source, headers=1) as stream:
        with pytest.raises(exceptions.FormatError) as excinfo:
            stream.save(target)
        assert 'xls' in str(excinfo.value)
