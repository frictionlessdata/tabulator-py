# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import io
import ast
import six
import pytest
import datetime
from sqlalchemy import create_engine
from tabulator import Stream, exceptions
from tabulator.loaders.local import LocalLoader
from tabulator.parsers.csv import CSVParser
from tabulator.writers.csv import CSVWriter
BASE_URL = 'https://raw.githubusercontent.com/okfn/tabulator-py/master/%s'


# Headers

def test_stream_headers():
    with Stream('data/table.csv', headers=1) as stream:
        assert stream.headers == ['id', 'name']
        assert list(stream.iter(keyed=True)) == [
            {'id': '1', 'name': 'english'},
            {'id': '2', 'name': '中国人'}]


def test_stream_headers_user_set():
    source = [['1', 'english'], ['2', '中国人']]
    with Stream(source, headers=['id', 'name']) as stream:
        assert stream.headers == ['id', 'name']
        assert list(stream.iter(keyed=True)) == [
            {'id': '1', 'name': 'english'},
            {'id': '2', 'name': '中国人'}]


def test_stream_headers_stream_context_manager():
    source = io.open('data/table.csv', mode='rb')
    with Stream(source, headers=1, format='csv') as stream:
        assert stream.headers == ['id', 'name']
        assert stream.read(extended=True) == [
            (2, ['id', 'name'], ['1', 'english']),
            (3, ['id', 'name'], ['2', '中国人'])]


def test_stream_headers_inline():
    source = [[], ['id', 'name'], ['1', 'english'], ['2', '中国人']]
    with Stream(source, headers=2) as stream:
        assert stream.headers == ['id', 'name']
        assert stream.read(extended=True) == [
            (3, ['id', 'name'], ['1', 'english']),
            (4, ['id', 'name'], ['2', '中国人'])]


def test_stream_headers_json_keyed():
    # Get table
    source = ('text://['
        '{"id": 1, "name": "english"},'
        '{"id": 2, "name": "中国人"}]')
    with Stream(source, headers=1, format='json') as stream:
        assert stream.headers == ['id', 'name']
        assert list(stream.iter(keyed=True)) == [
            {'id': 1, 'name': 'english'},
            {'id': 2, 'name': '中国人'}]


def test_stream_headers_inline_keyed():
    source = [{'id': '1', 'name': 'english'}, {'id': '2', 'name': '中国人'}]
    with Stream(source, headers=1) as stream:
        assert stream.headers == ['id', 'name']
        assert list(stream.iter(keyed=True)) == [
            {'id': '1', 'name': 'english'},
            {'id': '2', 'name': '中国人'}]


def test_stream_headers_inline_keyed_headers_is_none():
    source = [{'id': '1', 'name': 'english'}, {'id': '2', 'name': '中国人'}]
    with Stream(source, headers=None) as stream:
        assert stream.headers == None
        assert list(stream.iter(extended=True)) == [
            (1, None, ['1', 'english']),
            (2, None, ['2', '中国人'])]


# Scheme: local

def test_stream_local():
    with Stream('data/table.csv') as stream:
        assert stream.read() == [['id', 'name'], ['1', 'english'], ['2', '中国人']]


# Scheme: remote

def test_stream_remote():
    with Stream(BASE_URL % 'data/table.csv') as stream:
        assert stream.read() == [['id', 'name'], ['1', 'english'], ['2', '中国人']]


# Scheme: stream

def test_stream_stream():
    source = io.open('data/table.csv', mode='rb')
    with Stream(source, format='csv') as stream:
        assert stream.read() == [['id', 'name'], ['1', 'english'], ['2', '中国人']]


# Scheme: text

def test_stream_text():
    source = 'text://value1,value2\nvalue3,value4'
    with Stream(source, format='csv') as stream:
        assert stream.read() == [['value1', 'value2'], ['value3', 'value4']]


# Format: csv

def test_stream_local_csv():
    with Stream('data/table.csv') as stream:
        assert stream.headers is None
        assert stream.read() == [['id', 'name'], ['1', 'english'], ['2', '中国人']]


def test_stream_local_csv_with_bom():
    with Stream('data/special/bom.csv') as stream:
        assert stream.headers is None
        assert stream.read() == [['id', 'name'], ['1', 'english'], ['2', '中国人']]


def test_stream_local_csv_with_bom_with_encoding():
    with Stream('data/special/bom.csv', encoding='utf-8') as stream:
        assert stream.headers is None
        assert stream.read() == [['id', 'name'], ['1', 'english'], ['2', '中国人']]


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


def test_stream_csv_doublequote():
    with Stream('data/special/doublequote.csv') as stream:
        for row in  stream:
            assert len(row) == 17


def test_stream_stream_csv():
    source = io.open('data/table.csv', mode='rb')
    with Stream(source, format='csv') as stream:
        assert stream.headers is None
        assert stream.read() == [['id', 'name'], ['1', 'english'], ['2', '中国人']]


def test_stream_text_csv():
    source = 'text://id,name\n1,english\n2,中国人\n'
    with Stream(source, format='csv') as stream:
        assert stream.headers is None
        assert stream.read() == [['id', 'name'], ['1', 'english'], ['2', '中国人']]


def test_stream_remote_csv():
    with Stream(BASE_URL % 'data/table.csv') as stream:
        assert stream.headers is None
        assert stream.read() == [['id', 'name'], ['1', 'english'], ['2', '中国人']]


def test_stream_remote_csv_non_ascii_url():
    with Stream('http://data.defra.gov.uk/ops/government_procurement_card/over_£500_GPC_apr_2013.csv') as stream:
        assert stream.sample[0] == [
            'Entity',
            'Transaction Posting Date',
            'Merchant Name',
            'Amount',
            'Description']


# Format: json

def test_stream_local_json_dicts():
    with Stream('data/table-dicts.json') as stream:
        assert stream.headers is None
        assert stream.read() == [[1, 'english'], [2, '中国人']]


def test_stream_local_json_lists():
    with Stream('data/table-lists.json') as stream:
        assert stream.headers is None
        assert stream.read() == [['id', 'name'], [1, 'english'], [2, '中国人']]


def test_stream_text_json_dicts():
    source = '[{"id": 1, "name": "english" }, {"id": 2, "name": "中国人" }]'
    with Stream(source, scheme='text', format='json') as stream:
        assert stream.headers is None
        assert stream.read() == [[1, 'english'], [2, '中国人']]


def test_stream_text_json_lists():
    source = '[["id", "name"], [1, "english"], [2, "中国人"]]'
    with Stream(source, scheme='text', format='json') as stream:
        assert stream.headers is None
        assert stream.read() == [['id', 'name'], [1, 'english'], [2, '中国人']]


def test_stream_remote_json_dicts():
    with Stream(BASE_URL % 'data/table-dicts.json') as stream:
        assert stream.headers is None
        assert stream.read() == [[1, 'english'], [2, '中国人']]


def test_stream_remote_json_lists():
    with Stream(BASE_URL % 'data/table-lists.json') as stream:
        assert stream.headers is None
        assert stream.read() == [['id', 'name'], [1, 'english'], [2, '中国人']]


# Format: ods

def test_stream_ods_remote():
    source = BASE_URL % 'data/table.ods'
    with Stream(source) as stream:
        assert stream.read() == [['id', 'name'], [1.0, 'english'], [2.0, '中国人']]


# Format: sql

def test_stream_format_sql(database_url):
    with Stream(database_url, table='data') as stream:
        assert stream.read() == [[1, 'english'], [2, '中国人']]


def test_stream_format_sql_order_by(database_url):
    with Stream(database_url, table='data', order_by='id') as stream:
        assert stream.read() == [[1, 'english'], [2, '中国人']]


def test_stream_format_sql_order_by_desc(database_url):
    with Stream(database_url, table='data', order_by='id desc') as stream:
        assert stream.read() == [[2, '中国人'], [1, 'english']]


def test_stream_format_sql_table_is_required_error(database_url):
    with pytest.raises(exceptions.OptionsError) as excinfo:
        Stream(database_url).open()
    assert 'table' in str(excinfo.value)


def test_stream_format_sql_headers(database_url):
    with Stream(database_url, table='data', headers=1) as stream:
        assert stream.headers == ['id', 'name']
        assert stream.read() == [[1, 'english'], [2, '中国人']]


# Format: xls

def test_stream_local_xls():
    with Stream('data/table.xls') as stream:
        assert stream.headers is None
        assert stream.read() == [['id', 'name'], [1.0, 'english'], [2.0, '中国人']]


def test_stream_remote_xls():
    with Stream(BASE_URL % 'data/table.xls') as stream:
        assert stream.headers is None
        assert stream.read() == [['id', 'name'], [1.0, 'english'], [2.0, '中国人']]


# Format: xlsx

def test_stream_xlsx_remote():
    source = BASE_URL % 'data/table.xlsx'
    with Stream(source) as stream:
        assert stream.read() == [['id', 'name'], [1.0, 'english'], [2.0, '中国人']]


def test_stream_stream_xlsx():
    source = io.open('data/table.xlsx', mode='rb')
    with Stream(source, format='xlsx') as stream:
        assert stream.headers is None
        assert stream.read() == [['id', 'name'], [1.0, 'english'], [2.0, '中国人']]


# Format: gsheet

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


# Format: inline

def test_stream_inline():
    source = [['id', 'name'], ['1', 'english'], ['2', '中国人']]
    with Stream(source) as stream:
        assert stream.headers is None
        assert stream.read() == [['id', 'name'], ['1', 'english'], ['2', '中国人']]


def test_stream_inline_iterator():
    source = iter([['id', 'name'], ['1', 'english'], ['2', '中国人']])
    with Stream(source) as stream:
        assert stream.headers is None
        assert stream.read() == [['id', 'name'], ['1', 'english'], ['2', '中国人']]


def test_stream_inline_iterator():
    def generator():
        yield ['id', 'name']
        yield ['1', 'english']
        yield ['2', '中国人']
    with pytest.raises(exceptions.SourceError) as excinfo:
        iterator = generator()
        Stream(iterator).open()
    assert 'callable' in str(excinfo.value)


def test_stream_inline_generator():
    def generator():
        yield ['id', 'name']
        yield ['1', 'english']
        yield ['2', '中国人']
    with Stream(generator) as stream:
        assert stream.headers is None
        assert stream.read() == [['id', 'name'], ['1', 'english'], ['2', '中国人']]


def test_stream_inline_keyed():
    source = [{'id': '1', 'name': 'english'}, {'id': '2', 'name': '中国人'}]
    with Stream(source, format='inline') as stream:
        assert stream.headers is None
        assert stream.read() == [['1', 'english'], ['2', '中国人']]


# Encoding

def test_stream_encoding():
    with Stream('data/table.csv', encoding='utf-8') as stream:
        assert stream.read() == [['id', 'name'], ['1', 'english'], ['2', '中国人']]


# Sample size

def test_stream_sample():
    source = [['id', 'name'], ['1', 'english'], ['2', '中国人']]
    with Stream(source, headers=1) as stream:
        assert stream.headers == ['id', 'name']
        assert stream.sample == [['1', 'english'], ['2', '中国人']]


# Allow html

def test_stream_html_content():
    # Link to html file containing information about csv file
    source = 'https://github.com/frictionlessdata/tabulator-py/blob/master/data/table.csv'
    with pytest.raises(exceptions.FormatError) as excinfo:
        Stream(source).open()
    assert 'HTML' in str(excinfo.value)


def test_stream_html_content_with_allow_html():
    # Link to html file containing information about csv file
    source = 'https://github.com/frictionlessdata/tabulator-py/blob/master/data/table.csv'
    with Stream(source, allow_html=True) as stream:
        assert stream


# Force strings

def test_stream_force_strings():
    temp = datetime.datetime(2000, 1, 1, 17)
    date = datetime.date(2000, 1, 1)
    time = datetime.time(17, 00)
    source = [['John', 21, 1.5, temp, date, time]]
    with Stream(source, force_strings=True) as stream:
        assert stream.read() == [
            ['John', '21', '1.5', '2000-01-01T17:00:00', '2000-01-01', '17:00:00']
        ]


# Force parse

def test_stream_force_parse_inline():
    source = [['John', 21], 'bad-row', ['Alex', 33]]
    with Stream(source, force_parse=True) as stream:
        assert stream.read(extended=True) == [
            (1, None, ['John', 21]),
            (2, None, []),
            (3, None, ['Alex', 33]),
        ]


def test_stream_force_parse_json():
    source = '[["John", 21], "bad-row", ["Alex", 33]]'
    with Stream(source, scheme='text', format='json', force_parse=True) as stream:
        assert stream.read(extended=True) == [
            (1, None, ['John', 21]),
            (2, None, []),
            (3, None, ['Alex', 33]),
        ]


# Skip rows


def test_stream_skip_rows():
    source = 'data/special/skip-rows.csv'
    with Stream(source, skip_rows=['#', 4]) as stream:
        assert stream.read() == [['id', 'name'], ['1', 'english']]


def test_stream_skip_rows_with_headers():
    source = 'data/special/skip-rows.csv'
    with Stream(source, headers=2, skip_rows=['#', 1]) as stream:
        assert stream.read() == [['2', '中国人']]


# Post parse

def test_stream_post_parse_headers():

    # Processors
    def extract_headers(extended_rows):
        headers = None
        for row_number, _, row in extended_rows:
            if row_number == 1:
                headers = row
                continue
            yield (row_number, headers, row)

    # Stream
    source = [['id', 'name'], ['1', 'english'], ['2', '中国人']]
    with Stream(source, post_parse=[extract_headers]) as stream:
        assert stream.headers == None
        assert stream.read(extended=True) == [
            (2, ['id', 'name'], ['1', 'english']),
            (3, ['id', 'name'], ['2', '中国人'])]


def test_stream_post_parse_chain():

    # Processors
    def skip_commented_rows(extended_rows):
        for row_number, headers, row in extended_rows:
            if (row and hasattr(row[0], 'startswith') and
                    row[0].startswith('#')):
                continue
            yield (row_number, headers, row)
    def skip_blank_rows(extended_rows):
        for row_number, headers, row in extended_rows:
            if not row:
                continue
            yield (row_number, headers, row)
    def cast_rows(extended_rows):
        for row_number, headers, row in extended_rows:
            crow = []
            for value in row:
                try:
                    if isinstance(value, six.string_types):
                        value = ast.literal_eval(value)
                except Exception:
                    pass
                crow.append(value)
            yield (row_number, headers, crow)

    # Stream
    source = [['id', 'name'], ['#1', 'english'], [], ['2', '中国人']]
    post_parse = [skip_commented_rows, skip_blank_rows, cast_rows]
    with Stream(source, headers=1, post_parse=post_parse) as stream:
        assert stream.headers == ['id', 'name']
        assert stream.read() == [[2, '中国人']]


def test_stream_post_parse_sample():

    # Processors
    def only_first_row(extended_rows):
        for row_number, header, row in extended_rows:
            if row_number == 1:
                yield (row_number, header, row)

    # Stream
    with Stream('data/table.csv', post_parse=[only_first_row]) as stream:
        assert stream.sample == [['id', 'name']]


# Custom loaders


def test_stream_custom_loaders():
    source = 'custom://data/table.csv'
    class CustomLoader(LocalLoader):
        def load(self, source, *args, **kwargs):
            return super(CustomLoader, self).load(
                source.replace('custom://', ''), *args, **kwargs)
    with Stream(source, custom_loaders={'custom': CustomLoader}) as stream:
        assert stream.read() == [['id', 'name'], ['1', 'english'], ['2', '中国人']]


# Custom parsers


def test_stream_custom_parsers():
    source = 'data/table.custom'
    class CustomParser(CSVParser):
        def open(self, source, *args, **kwargs):
            return super(CustomParser, self).open(
                source.replace('custom', 'csv'), *args, **kwargs)
    with Stream(source, custom_parsers={'custom': CustomParser}) as stream:
        assert stream.read() == [['id', 'name'], ['1', 'english'], ['2', '中国人']]


# Custom writers

def test_stream_save_custom_writers(tmpdir):
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


# Loader/parser options

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


def test_stream_json_node():
    source = '{"root": [["value1", "value2"], ["value3", "value4"]]}'
    with Stream(source, scheme='text', format='json', node='root') as stream:
        assert stream.read() == [['value1', 'value2'], ['value3', 'value4']]


# Open errors

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


# Reset

def test_stream_reset():
    with Stream('data/table.csv', headers=1) as stream:
        headers1 = stream.headers
        contents1 = stream.read()
        stream.reset()
        headers2 = stream.headers
        contents2 = stream.read()
        assert headers1 == ['id', 'name']
        assert contents1 == [['1', 'english'], ['2', '中国人']]
        assert headers1 == headers2
        assert contents1 == contents2


def test_stream_reset_and_sample_size():
    with Stream('data/special/long.csv', headers=1, sample_size=3) as stream:
        # Before reset
        assert stream.read(extended=True) == [
            (2, ['id', 'name'], ['1', 'a']),
            (3, ['id', 'name'], ['2', 'b']),
            (4, ['id', 'name'], ['3', 'c']),
            (5, ['id', 'name'], ['4', 'd']),
            (6, ['id', 'name'], ['5', 'e']),
            (7, ['id', 'name'], ['6', 'f'])]
        assert stream.sample == [['1', 'a'], ['2', 'b']]
        assert stream.read() == []
        # Reset stream
        stream.reset()
        # After reset
        assert stream.read(extended=True, limit=3) == [
            (2, ['id', 'name'], ['1', 'a']),
            (3, ['id', 'name'], ['2', 'b']),
            (4, ['id', 'name'], ['3', 'c'])]
        assert stream.sample == [['1', 'a'], ['2', 'b']]
        assert stream.read(extended=True) == [
            (5, ['id', 'name'], ['4', 'd']),
            (6, ['id', 'name'], ['5', 'e']),
            (7, ['id', 'name'], ['6', 'f'])]


def test_stream_reset_generator():
    def generator():
        yield [1]
        yield [2]
    with Stream(generator, sample_size=0) as stream:
        # Before reset
        assert stream.read() == [[1], [2]]
        # Reset stream
        stream.reset()
        # After reset
        assert stream.read() == [[1], [2]]

# Save

def test_stream_save_csv(tmpdir):
    source = 'data/table.csv'
    target = str(tmpdir.join('table.csv'))
    with Stream(source, headers=1) as stream:
        stream.save(target)
    with Stream(target, headers=1) as stream:
        assert stream.headers == ['id', 'name']
        assert stream.read(extended=True) == [
            (2, ['id', 'name'], ['1', 'english']),
            (3, ['id', 'name'], ['2', '中国人'])]


def test_stream_save_xls(tmpdir):
    source = 'data/table.csv'
    target = str(tmpdir.join('table.xls'))
    with Stream(source, headers=1) as stream:
        with pytest.raises(exceptions.FormatError) as excinfo:
            stream.save(target)
        assert 'xls' in str(excinfo.value)
