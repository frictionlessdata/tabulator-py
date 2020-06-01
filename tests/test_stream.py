# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import io
import ast
import six
import sys
import pytest
import datetime
from sqlalchemy import create_engine
from tabulator import Stream, exceptions
from tabulator.loaders.local import LocalLoader
from tabulator.parsers.csv import CSVParser
from tabulator.writers.csv import CSVWriter
from tabulator.writers.xlsx import XLSXWriter
BASE_URL = 'https://raw.githubusercontent.com/frictionlessdata/tabulator-py/master/%s'


# General

def test_stream():
    with Stream('data/table.csv') as stream:
        assert stream.source == 'data/table.csv'
        assert stream.scheme == 'file'
        assert stream.format == 'csv'
        assert stream.encoding == 'utf-8'
        assert stream.compression == 'no'


# Headers

def test_stream_headers():
    with Stream('data/table.csv', headers=1) as stream:
        assert stream.headers == ['id', 'name']
        assert list(stream.iter(keyed=True)) == [
            {'id': '1', 'name': 'english'},
            {'id': '2', 'name': '中国人'}]


def test_stream_headers_unicode():
    with Stream('data/table_unicode_headers.csv', headers=1) as stream:
        assert stream.headers == ['id', '国人']
        assert list(stream.iter(keyed=True)) == [
            {'id': '1', '国人': 'english'},
            {'id': '2', '国人': '中国人'}]


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


def test_stream_headers_xls_multiline():
    source = 'data/special/multiline-headers.xlsx'
    with Stream(source, headers=[1, 5], fill_merged_cells=True) as stream:
        assert stream.headers == [
            'Region',
            'Caloric contribution (%)',
            'Cumulative impact of changes on cost of food basket from previous quarter',
            'Cumulative impact of changes on cost of food basket from baseline (%)',
        ]
        assert stream.read() == [
            ['A', 'B', 'C', 'D']
        ]


def test_stream_headers_csv_multiline_headers_joiner():
    source = 'text://k1\nk2\nv1\nv2\nv3'
    with Stream(source, format='csv', headers=[1, 2], multiline_headers_joiner=':') as stream:
        assert stream.headers == ['k1:k2']
        assert stream.read() == [['v1'], ['v2'], ['v3']]


def test_stream_headers_csv_multiline_headers_duplicates():
    source = 'text://k1\nk1\nv1\nv2\nv3'
    with Stream(source, format='csv', headers=[1, 2], multiline_headers_duplicates=True) as stream:
        assert stream.headers == ['k1 k1']
        assert stream.read() == [['v1'], ['v2'], ['v3']]


def test_stream_headers_strip_and_non_strings():
    source = [[' header ', 2, 3, None], ['value1', 'value2', 'value3', 'value4']]
    with Stream(source, headers=1) as stream:
        assert stream.headers == ['header', '2', '3', '']
        assert stream.read() == [['value1', 'value2', 'value3', 'value4']]


def test_stream_headers_set_property():
    with Stream('data/table.csv', headers=1) as stream:
        stream.headers = ['number', 'language']
        assert stream.headers == ['number', 'language']
        assert list(stream.iter(keyed=True)) == [
            {'number': '1', 'language': 'english'},
            {'number': '2', 'language': '中国人'}]


# Compression errors

def test_stream_compression_error_gz():
    source = 'id,filename\n\1,dump.tar.gz'
    stream = Stream(source, scheme='text', format='csv')
    stream.open()

def test_stream_compression_error_zip():
    source = 'id,filename\n1,archive.zip'
    stream = Stream(source, scheme='text', format='csv')
    stream.open()


# Scheme

def test_stream_scheme_file():
    with Stream('data/table.csv') as stream:
        assert stream.scheme == 'file'


@pytest.mark.remote
def test_stream_scheme_https():
    with Stream(BASE_URL % 'data/table.csv') as stream:
        assert stream.scheme == 'https'


def test_stream_scheme_stream():
    with Stream(io.open('data/table.csv', mode='rb'), format='csv') as stream:
        assert stream.scheme == 'stream'


def test_stream_scheme_text():
    with Stream('text://a\nb', format='csv') as stream:
        assert stream.scheme == 'text'


# Format

def test_stream_format_csv():
    with Stream('data/table.csv') as stream:
        assert stream.format == 'csv'


def test_stream_format_ndjson():
    with Stream('data/table.ndjson') as stream:
        assert stream.format == 'ndjson'


def test_stream_format_ods():
    with Stream('data/table.ods') as stream:
        assert stream.format == 'ods'


def test_stream_format_tsv():
    with Stream('data/table.tsv') as stream:
        assert stream.format == 'tsv'


def test_stream_format_xls():
    with Stream('data/table.xls') as stream:
        assert stream.format == 'xls'


def test_stream_format_xlsx():
    with Stream('data/table.xlsx') as stream:
        assert stream.format == 'xlsx'

def test_stream_format_html():
    with Stream('data/table1.html') as stream:
        assert stream.format == 'html'


# Encoding

def test_stream_encoding():
    with Stream('data/table.csv') as stream:
        assert stream.encoding == 'utf-8'
        assert stream.read() == [['id', 'name'], ['1', 'english'], ['2', '中国人']]


def test_stream_encoding_explicit_utf8():
    with Stream('data/table.csv', encoding='utf-8') as stream:
        assert stream.encoding == 'utf-8'
        assert stream.read() == [['id', 'name'], ['1', 'english'], ['2', '中国人']]


def test_stream_encoding_explicit_latin1():
    with Stream('data/special/latin1.csv', encoding='latin1') as stream:
        assert stream.encoding == 'iso8859-1'
        assert stream.read() == [['id', 'name'], ['1', 'english'], ['2', '©']]


def test_stream_encoding_utf_16():
    # Bytes encoded as UTF-16 with BOM in platform order is detected
    bio = io.BytesIO(u'en,English\nja,日本語'.encode('utf-16'))
    with Stream(bio, format='csv') as stream:
        assert stream.encoding == 'utf-16'
        assert stream.read() == [[u'en', u'English'], [u'ja', u'日本語']]


def test_stream_encoding_missmatch_handle_errors():
    with pytest.raises(exceptions.EncodingError) as excinfo:
        with Stream('data/table.csv', encoding='ascii') as stream:
            stream.read()
    assert str(excinfo.value) == 'Cannot parse the source "data/table.csv" using "ascii" encoding at "20"'


# Allow html

@pytest.mark.remote
def test_stream_html_content():
    # Link to html file containing information about csv file
    source = 'https://github.com/frictionlessdata/tabulator-py/blob/master/data/table.csv'
    with pytest.raises(exceptions.FormatError) as excinfo:
        Stream(source).open()
    assert 'HTML' in str(excinfo.value)


@pytest.mark.remote
def test_stream_html_content_with_allow_html():
    # Link to html file containing information about csv file
    source = 'https://github.com/frictionlessdata/tabulator-py/blob/master/data/table.csv'
    with Stream(source, allow_html=True) as stream:
        assert stream


# Sample size

def test_stream_sample():
    source = [['id', 'name'], ['1', 'english'], ['2', '中国人']]
    with Stream(source, headers=1) as stream:
        assert stream.headers == ['id', 'name']
        assert stream.sample == [['1', 'english'], ['2', '中国人']]


# Bytes sample size

def test_stream_bytes_sample_size():
    source = 'data/special/latin1.csv'
    with Stream(source) as stream:
        try:
            import cchardet
            assert stream.encoding == 'cp1252'
        except ImportError:
            assert stream.encoding == 'iso8859-1'
    with Stream(source, sample_size=0, bytes_sample_size=10) as stream:
        assert stream.encoding == 'utf-8'


# Ignore blank headers

def test_stream_ignore_blank_headers_false():
    source = 'text://header1,,header3\nvalue1,value2,value3'
    with Stream(source, format='csv', headers=1) as stream:
        assert stream.headers == ['header1', '', 'header3']
        assert stream.read(keyed=True) == [
            {'header1': 'value1', '': 'value2', 'header3': 'value3'},
        ]


def test_stream_ignore_blank_headers_true():
    source = 'text://header1,,header3,,header5\nvalue1,value2,value3,value4,value5'
    data = [
            {'header1': 'value1',
             'header3': 'value3',
             'header5': 'value5'},
        ]
    with Stream(source, format='csv', headers=1, ignore_blank_headers=True) as stream:
        assert stream.headers == ['header1', 'header3', 'header5']
        assert stream.sample == [['value1', 'value3', 'value5']]
        assert stream.sample == [['value1', 'value3', 'value5']]
        assert stream.read(keyed=True) == data
        stream.close()
        stream.open()
        assert stream.read(keyed=True) == data


# Ignore listed/not_listed headers

def test_stream_ignore_listed_headers():
    source = 'text://header1,header2,header3\nvalue1,value2,value3'
    with Stream(source, format='csv', headers=1, ignore_listed_headers=['header2']) as stream:
        assert stream.headers == ['header1', 'header3']
        assert stream.read(keyed=True) == [
            {'header1': 'value1', 'header3': 'value3'},
        ]


def test_stream_ignore_not_listed_headers():
    source = 'text://header1,header2,header3\nvalue1,value2,value3'
    with Stream(source, format='csv', headers=1, ignore_not_listed_headers=['header2']) as stream:
        assert stream.headers == ['header2']
        assert stream.read(keyed=True) == [
            {'header2': 'value2'},
        ]


# Skip/pick fields

def test_stream_skip_fields():
    source = 'text://header1,header2,header3\nvalue1,value2,value3'
    with Stream(source, format='csv', headers=1, skip_fields=['header2']) as stream:
        assert stream.headers == ['header1', 'header3']
        assert stream.field_positions == [1, 3]
        assert stream.read(keyed=True) == [
            {'header1': 'value1', 'header3': 'value3'},
        ]


def test_stream_skip_fields_position():
    source = 'text://header1,header2,header3\nvalue1,value2,value3'
    with Stream(source, format='csv', headers=1, skip_fields=[2]) as stream:
        assert stream.headers == ['header1', 'header3']
        assert stream.field_positions == [1, 3]
        assert stream.read(keyed=True) == [
            {'header1': 'value1', 'header3': 'value3'},
        ]


def test_stream_skip_fields_position_and_prefix():
    source = 'text://header1,header2,header3\nvalue1,value2,value3'
    with Stream(source, format='csv', headers=1, skip_fields=[2, 'header3']) as stream:
        assert stream.headers == ['header1']
        assert stream.field_positions == [1]
        assert stream.read(keyed=True) == [
            {'header1': 'value1'},
        ]


def test_stream_skip_fields_blank_header():
    source = 'text://header1,,header3\nvalue1,value2,value3'
    with Stream(source, format='csv', headers=1, skip_fields=['']) as stream:
        assert stream.headers == ['header1', 'header3']
        assert stream.field_positions == [1, 3]
        assert stream.read(keyed=True) == [
            {'header1': 'value1', 'header3': 'value3'},
        ]


def test_stream_pick_fields():
    source = 'text://header1,header2,header3\nvalue1,value2,value3'
    with Stream(source, format='csv', headers=1, pick_fields=['header2']) as stream:
        assert stream.headers == ['header2']
        assert stream.field_positions == [2]
        assert stream.read(keyed=True) == [
            {'header2': 'value2'},
        ]


def test_stream_pick_fields_position():
    source = 'text://header1,header2,header3\nvalue1,value2,value3'
    with Stream(source, format='csv', headers=1, pick_fields=[2]) as stream:
        assert stream.headers == ['header2']
        assert stream.field_positions == [2]
        assert stream.read(keyed=True) == [
            {'header2': 'value2'},
        ]


def test_stream_pick_fields_position_and_prefix():
    source = 'text://header1,header2,header3\nvalue1,value2,value3'
    with Stream(source, format='csv', headers=1, pick_fields=[2, 'header3']) as stream:
        assert stream.headers == ['header2', 'header3']
        assert stream.field_positions == [2, 3]
        assert stream.read(keyed=True) == [
            {'header2': 'value2', 'header3': 'value3'},
        ]


# Skip/pick columns

def test_stream_skip_columns():
    source = 'text://header1,header2,header3\nvalue1,value2,value3'
    with Stream(source, format='csv', headers=1, skip_columns=['header2']) as stream:
        assert stream.headers == ['header1', 'header3']
        assert stream.read(keyed=True) == [
            {'header1': 'value1', 'header3': 'value3'},
        ]


def test_stream_skip_columns_blank_header():
    source = 'text://header1,,header3\nvalue1,value2,value3'
    with Stream(source, format='csv', headers=1, skip_columns=['']) as stream:
        assert stream.headers == ['header1', 'header3']
        assert stream.read(keyed=True) == [
            {'header1': 'value1', 'header3': 'value3'},
        ]


def test_stream_pick_columns():
    source = 'text://header1,header2,header3\nvalue1,value2,value3'
    with Stream(source, format='csv', headers=1, pick_columns=['header2']) as stream:
        assert stream.headers == ['header2']
        assert stream.read(keyed=True) == [
            {'header2': 'value2'},
        ]


# Force strings

def test_stream_force_strings():
    temp = datetime.datetime(2000, 1, 1, 17)
    date = datetime.date(2000, 1, 1)
    time = datetime.time(17, 00)
    source = [['John', 21, 1.5, temp, date, time]]
    with Stream(source, force_strings=True) as stream:
        assert stream.read() == [
            ['John', '21', '1.5', '2000-01-01T17:00:00', '2000-01-01',
             '17:00:00']
        ]
        assert stream.sample == [
            ['John', '21', '1.5', '2000-01-01T17:00:00', '2000-01-01',
             '17:00:00']
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


# Pick rows

def test_stream_pick_rows():
    source = 'data/special/skip-rows.csv'
    with Stream(source, pick_rows=['1', '2']) as stream:
        assert stream.read() == [['1', 'english'], ['2', '中国人']]


def test_stream_pick_rows_number():
    source = 'data/special/skip-rows.csv'
    with Stream(source, pick_rows=[3, 5]) as stream:
        assert stream.read() == [['1', 'english'], ['2', '中国人']]


def test_stream_pick_rows_regex():
    source = [['# comment'], ['name', 'order'], ['# cat'], ['# dog'], ['John', 1], ['Alex', 2]]
    pick_rows = [{'type': 'regex', 'value': r'^(name|John|Alex)'}]
    with Stream(source, headers=1, pick_rows=pick_rows) as stream:
        assert stream.headers == ['name', 'order']
        assert stream.read() == [['John', 1], ['Alex', 2]]


# Skip rows

def test_stream_skip_rows():
    source = 'data/special/skip-rows.csv'
    with Stream(source, skip_rows=['#', 5]) as stream:
        assert stream.read() == [['id', 'name'], ['1', 'english']]


def test_stream_skip_rows_from_the_end():
    source = 'data/special/skip-rows.csv'
    with Stream(source, skip_rows=[1, -2]) as stream:
        assert stream.read() == [['id', 'name'], ['1', 'english'], ['2', '中国人']]
    with Stream(source, skip_rows=[1, -1, -2]) as stream:
        assert stream.read() == [['id', 'name'], ['1', 'english']]


def test_stream_skip_rows_no_double_skip():
    source = 'data/special/skip-rows.csv'
    with Stream(source, skip_rows=[1, 4, -2]) as stream:
        assert stream.read() == [['id', 'name'], ['1', 'english'], ['2', '中国人']]
    # no double skip at the very last row
    with Stream(source, skip_rows=[1, 5, -1]) as stream:
        assert stream.read() == [['id', 'name'], ['1', 'english'], ["# it's a comment!"]]


def test_stream_skip_rows_excel_empty_column():
    source = 'data/special/skip-rows.xlsx'
    with Stream(source, headers=1, skip_rows=['']) as stream:
        assert stream.read() == [['A', 'B'], [8, 9]]


def test_stream_skip_rows_with_headers():
    source = 'data/special/skip-rows.csv'
    with Stream(source, headers=1, skip_rows=['#']) as stream:
        assert stream.headers == ['id', 'name']
        assert stream.read() == [['1', 'english'], ['2', '中国人']]


def test_stream_skip_rows_with_headers_example_from_readme():
    source = [['#comment'], ['name', 'order'], ['John', 1], ['Alex', 2]]
    with Stream(source, headers=1, skip_rows=['#']) as stream:
        assert stream.headers == ['name', 'order']
        assert stream.read() == [['John', 1], ['Alex', 2]]


def test_stream_skip_rows_regex():
    source = [['# comment'], ['name', 'order'], ['# cat'], ['# dog'], ['John', 1], ['Alex', 2]]
    skip_rows = ['# comment', {'type': 'regex', 'value': r'^# (cat|dog)'}]
    with Stream(source, headers=1, skip_rows=skip_rows) as stream:
        assert stream.headers == ['name', 'order']
        assert stream.read() == [['John', 1], ['Alex', 2]]


def test_stream_skip_rows_preset():
    source = [['name', 'order'], ['', ''], [], ['Ray', 0], ['John', 1], ['Alex', 2], ['', 3], [None, 4], ['', None]]
    skip_rows = [{'type': 'preset', 'value': 'blank'}]
    with Stream(source, headers=1, skip_rows=skip_rows) as stream:
        assert stream.headers == ['name', 'order']
        assert stream.read() == [['Ray', 0], ['John', 1], ['Alex', 2], ['', 3], [None, 4]]


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


def test_stream_json_property():
    source = '{"root": [["value1", "value2"], ["value3", "value4"]]}'
    with Stream(source, scheme='text', format='json', property='root') as stream:
        assert stream.read() == [['value1', 'value2'], ['value3', 'value4']]


# Open errors

def test_stream_source_error_data():
    stream = Stream('[1,2]', scheme='text', format='json')
    with pytest.raises(exceptions.SourceError) as excinfo:
        stream.open()
        stream.read()


def test_stream_format_error_html():
    stream = Stream('data/special/table.csv.html', format='csv')
    with pytest.raises(exceptions.FormatError) as excinfo:
        stream.open()


def test_stream_scheme_error():
    stream = Stream('', scheme='bad-scheme')
    with pytest.raises(exceptions.SchemeError) as excinfo:
        stream.open()
    assert 'bad-scheme' in str(excinfo.value)


def test_stream_format_error():
    stream = Stream('data/special/table.bad-format')
    with pytest.raises(exceptions.FormatError) as excinfo:
        stream.open()
    assert 'bad-format' in str(excinfo.value)


@pytest.mark.skipif(sys.version_info < (3, 5), reason='not supported')
def test_stream_bad_options_warning():
    Stream('', scheme='text', format='csv', bad_option=True).open()
    with pytest.warns(UserWarning) as record:
        Stream('', scheme='text', format='csv', bad_option=True).open()
    assert 'bad_option' in str(record[0].message.args[0])


def test_stream_io_error():
    stream = Stream('bad_path.csv')
    with pytest.raises(exceptions.IOError) as excinfo:
        stream.open()
    assert 'bad_path.csv' in str(excinfo.value)


def test_stream_http_error():
    stream = Stream('http://github.com/bad_path.csv')
    with pytest.raises(exceptions.HTTPError) as excinfo:
        stream.open()


# Stats

def test_stream_size():
    with Stream('data/special/doublequote.csv') as stream:
        rows = stream.read()
        assert stream.size == 7346


@pytest.mark.skipif(six.PY2, reason='Support only for Python3')
def test_stream_size_compressed():
    with Stream('data/special/doublequote.csv.zip') as stream:
        rows = stream.read()
        assert stream.size == 7346


@pytest.mark.remote
def test_stream_size_remote():
    with Stream(BASE_URL % 'data/special/doublequote.csv') as stream:
        rows = stream.read()
        assert stream.size == 7346


def test_stream_hash():
    with Stream('data/special/doublequote.csv') as stream:
        rows = stream.read()
        assert stream.hash == '41fdde1d8dbcb3b2d4a1410acd7ad842781f076076a73b049863d6c1c73868db'
        assert stream.hashing_algorithm == 'sha256'


def test_stream_hash_md5():
    with Stream('data/special/doublequote.csv', hashing_algorithm='md5') as stream:
        rows = stream.read()
        assert stream.hash == 'd82306001266c4343a2af4830321ead8'
        assert stream.hashing_algorithm == 'md5'


def test_stream_hash_sha1():
    with Stream('data/special/doublequote.csv', hashing_algorithm='sha1') as stream:
        rows = stream.read()
        assert stream.hash == '2842768834a6804d8644dd689da61c7ab71cbb33'
        assert stream.hashing_algorithm == 'sha1'


def test_stream_hash_sha256():
    with Stream('data/special/doublequote.csv', hashing_algorithm='sha256') as stream:
        rows = stream.read()
        assert stream.hash == '41fdde1d8dbcb3b2d4a1410acd7ad842781f076076a73b049863d6c1c73868db'
        assert stream.hashing_algorithm == 'sha256'


def test_stream_hash_sha512():
    with Stream('data/special/doublequote.csv', hashing_algorithm='sha512') as stream:
        rows = stream.read()
        assert stream.hash == 'fa555b28a01959c8b03996cd4757542be86293fd49641d61808e4bf9fe4115619754aae9ae6af6a0695585eaade4488ce00dfc40fc4394b6376cd20d6967769c'
        assert stream.hashing_algorithm == 'sha512'


def test_stream_hash_not_supported():
    with pytest.raises(AssertionError):
        with Stream('data/special/doublequote.csv', hashing_algorithm='bad') as stream:
            rows = stream.read()


@pytest.mark.skipif(six.PY2, reason='Support only for Python3')
def test_stream_hash_compressed():
    with Stream('data/special/doublequote.csv.zip') as stream:
        rows = stream.read()
        assert stream.hash == '41fdde1d8dbcb3b2d4a1410acd7ad842781f076076a73b049863d6c1c73868db'


@pytest.mark.remote
def test_stream_hash_remote():
    with Stream(BASE_URL % 'data/special/doublequote.csv') as stream:
        rows = stream.read()
        assert stream.hash == '41fdde1d8dbcb3b2d4a1410acd7ad842781f076076a73b049863d6c1c73868db'


# Field positions

def test_stream_field_positions():
    with Stream('data/table.csv', headers=1) as stream:
        assert stream.field_positions == [1, 2]


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

def test_stream_save_xls_not_supported(tmpdir):
    source = 'data/table.csv'
    target = str(tmpdir.join('table.xls'))
    with Stream(source, headers=1) as stream:
        with pytest.raises(exceptions.FormatError) as excinfo:
            stream.save(target)
        assert 'xls' in str(excinfo.value)


def test_stream_save_sqlite(database_url):
    source = 'data/table.csv'
    with Stream(source, headers=1) as stream:
        stream.save(database_url, table='test_stream_save_sqlite')
    with Stream(database_url, table='test_stream_save_sqlite', order_by='id', headers=1) as stream:
        assert stream.read() == [['1', 'english'], ['2', '中国人']]
        assert stream.headers == ['id', 'name']


# Reading closed

def test_stream_read_closed():
    stream = Stream('data/table.csv')
    with pytest.raises(exceptions.TabulatorException) as excinfo:
        stream.read()
    assert 'stream.open()' in str(excinfo.value)


# Support for compressed files

@pytest.mark.skipif(six.PY2, reason='Support only for Python3')
def test_stream_local_csv_zip():
    with Stream('data/table.csv.zip') as stream:
        assert stream.headers is None
        assert stream.compression == 'zip'
        assert stream.read() == [['id', 'name'], ['1', 'english'], ['2', '中国人']]


@pytest.mark.skipif(six.PY2, reason='Support only for Python3')
def test_stream_local_csv_zip_multiple_files():
    with Stream('data/2-files.zip', filename = 'table.csv') as stream:
        assert stream.headers is None
        assert stream.read() == [['id', 'name'], ['1', 'english'], ['2', '中国人']]
    with Stream('data/2-files.zip', filename = 'table-reverse.csv') as stream:
        assert stream.headers is None
        assert stream.read() == [['id', 'name'], ['1', '中国人'], ['2', 'english']]


@pytest.mark.skipif(six.PY2, reason='Support only for Python3')
def test_stream_local_csv_zip_multiple_open():
    # That's how `tableschema.iter()` acts
    stream = Stream('data/table.csv.zip')
    stream.open()
    assert stream.headers is None
    assert stream.read() == [['id', 'name'], ['1', 'english'], ['2', '中国人']]
    stream.close()
    stream.open()
    assert stream.headers is None
    assert stream.read() == [['id', 'name'], ['1', 'english'], ['2', '中国人']]
    stream.close()


@pytest.mark.skipif(six.PY2, reason='Support only for Python3')
def test_stream_local_csv_gz():
    with Stream('data/table.csv.gz') as stream:
        assert stream.headers is None
        assert stream.read() == [['id', 'name'], ['1', 'english'], ['2', '中国人']]


@pytest.mark.skipif(six.PY2, reason='Support only for Python3')
def test_stream_filelike_csv_zip():
    with open('data/table.csv.zip', 'rb') as file:
        with Stream(file, format='csv', compression='zip') as stream:
            assert stream.headers is None
            assert stream.read() == [['id', 'name'], ['1', 'english'], ['2', '中国人']]


@pytest.mark.skipif(six.PY2, reason='Support only for Python3')
def test_stream_filelike_csv_gz():
    with open('data/table.csv.gz', 'rb') as file:
        with Stream(file, format='csv', compression='gz') as stream:
            assert stream.headers is None
            assert stream.read() == [['id', 'name'], ['1', 'english'], ['2', '中国人']]


@pytest.mark.remote
@pytest.mark.skipif(six.PY2, reason='Support only for Python3')
def test_stream_remote_csv_zip():
    source = 'https://raw.githubusercontent.com/frictionlessdata/tabulator-py/master/data/table.csv.zip'
    with Stream(source) as stream:
        assert stream.headers is None
        assert stream.read() == [['id', 'name'], ['1', 'english'], ['2', '中国人']]


@pytest.mark.remote
@pytest.mark.skipif(six.PY2, reason='Support only for Python3')
def test_stream_remote_csv_gz():
    source = 'https://raw.githubusercontent.com/frictionlessdata/tabulator-py/master/data/table.csv.gz'
    with Stream(source) as stream:
        assert stream.headers is None
        assert stream.read() == [['id', 'name'], ['1', 'english'], ['2', '中国人']]


def test_stream_compression_invalid():
    with pytest.raises(exceptions.CompressionError) as excinfo:
        Stream('table.csv', compression='bad').open()
    assert 'bad' in str(excinfo.value)


# Issues

def test_stream_reset_on_close_issue_190():
    source = [['1', 'english'], ['2', '中国人']]
    stream = Stream(source)
    stream.open()
    stream.read(limit=1) == [['1', 'english']]
    stream.open()
    stream.read(limit=1) == [['1', 'english']]
    stream.close()


def test_stream_skip_blank_at_the_end_issue_bco_dmo_33():
    source = 'data/special/skip-blank-at-the-end.csv'
    with Stream(source, headers=1, skip_rows=['#']) as stream:
        assert stream.headers == ['test1', 'test2']
        assert stream.read() == [['1', '2'], []]


def test_stream_not_existent_local_file_with_no_format_issue_287():
    with pytest.raises(exceptions.IOError) as excinfo:
        Stream('bad-path').open()
    assert 'bad-path' in str(excinfo.value)


def test_stream_not_existent_remote_file_with_no_format_issue_287():
    with pytest.raises(exceptions.HTTPError) as excinfo:
        Stream('http://example.com/bad-path').open()
    assert 'bad-path' in str(excinfo.value)


@pytest.mark.remote
def test_stream_chardet_raises_remote_issue_305():
    source = 'https://gist.githubusercontent.com/roll/56b91d7d998c4df2d4b4aeeefc18cab5/raw/a7a577cd30139b3396151d43ba245ac94d8ddf53/tabulator-issue-305.csv'
    with Stream(source, headers=1) as stream:
        assert stream.encoding == 'utf-8'
        assert len(stream.read()) == 343


@pytest.mark.skip
def test_stream_wrong_encoding_detection_issue_265():
    with Stream('data/special/accent.csv') as stream:
        assert stream.encoding == 'utf-8'


def test_stream_skip_rows_non_string_cell_issue_322():
    source = [['id', 'name'], [1, 'english'], [2, 'spanish']]
    with Stream(source, headers=1, skip_rows='1') as stream:
        assert stream.headers == ['id', 'name']
        assert stream.read() == [[2, 'spanish']]


def test_stream_skip_rows_non_string_cell_issue_320():
    with Stream('data/special/issue320.xlsx', headers=[10, 12], fill_merged_cells=True) as stream:
        assert stream.headers[7] == 'Current Population Analysed % of total county Pop'
