# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import io
import ast
import sys
import six
import pytest
from tabulator import topen, parsers, exceptions


# Constants

BASE_URL = 'https://raw.githubusercontent.com/okfn/tabulator-py/master/%s'


# Tests [loaders/parsers]

def test_file_csv():

    # Get table
    table = topen('data/table.csv')

    # Make assertions
    assert table.headers is None
    assert table.read() == [['id', 'name'], ['1', 'english'], ['2', '中国人']]


def test_file_csv_parser_options():

    # Get table
    table = topen('data/table.csv',
            parser_options={'constructor': parsers.CSV})

    # Make assertions
    assert table.headers is None
    assert table.read() == [['id', 'name'], ['1', 'english'], ['2', '中国人']]

def test_file_csv_with_bom():

    # Get table
    table = topen('data/special/bom.csv', encoding='utf-8')

    # Make assertions
    assert table.headers is None
    assert table.read() == [['id', 'name'], ['1', 'english'], ['2', '中国人']]

    # Get table
    table = topen('data/special/bom.csv')

    # Make assertions
    assert table.headers is None
    assert table.read() == [['id', 'name'], ['1', 'english'], ['2', '中国人']]



# DEPRECATED [v0.5-v1)
def test_file_csv_parser_class():

    # Get table
    table = topen('data/table.csv', parser_class=parsers.CSV)

    # Make assertions
    assert table.headers is None
    assert table.read() == [['id', 'name'], ['1', 'english'], ['2', '中国人']]


def test_file_json_dicts():

    # Get table
    table = topen('data/table-dicts.json')

    # Make assertions
    assert table.headers is None
    assert table.read() == [[1, 'english'], [2, '中国人']]


def test_file_json_lists():

    # Get table
    table = topen('data/table-lists.json')

    # Make assertions
    assert table.headers is None
    assert table.read() == [['id', 'name'], [1, 'english'], [2, '中国人']]


def test_file_xls():

    # Get table
    table = topen('data/table.xls')

    # Make assertions
    assert table.headers is None
    assert table.read() == [['id', 'name'], [1.0, 'english'], [2.0, '中国人']]


def test_stream_csv():

    # Get table
    source = io.open('data/table.csv', mode='rb')
    table = topen(source, format='csv')

    # Make assertions
    assert table.headers is None
    assert table.read() == [['id', 'name'], ['1', 'english'], ['2', '中国人']]


def test_stream_xlsx():

    # Get table
    source = io.open('data/table.xlsx', mode='rb')
    table = topen(source, format='xlsx')

    # Make assertions
    assert table.headers is None
    assert table.read() == [['id', 'name'], [1.0, 'english'], [2.0, '中国人']]


def test_text_csv():

    # Get table
    source = 'text://id,name\n1,english\n2,中国人\n'
    table = topen(source, format='csv')

    # Make assertions
    assert table.headers is None
    assert table.read() == [['id', 'name'], ['1', 'english'], ['2', '中国人']]


def test_text_json_dicts():

    # Get table
    source = '[{"id": 1, "name": "english" }, {"id": 2, "name": "中国人" }]'
    table = topen(source, scheme='text', format='json')

    # Make assertions
    assert table.headers is None
    assert table.read() == [[1, 'english'], [2, '中国人']]


def test_text_json_lists():

    # Get table
    source = '[["id", "name"], [1, "english"], [2, "中国人"]]'
    table = topen(source, scheme='text', format='json')

    # Make assertions
    assert table.headers is None
    assert table.read() == [['id', 'name'], [1, 'english'], [2, '中国人']]


def test_web_csv():

    # Get table
    table = topen(BASE_URL % 'data/table.csv')

    # Make assertions
    assert table.headers is None
    assert table.read() == [['id', 'name'], ['1', 'english'], ['2', '中国人']]


def test_web_csv_non_ascii_url():

    # Get table
    table = topen('http://data.defra.gov.uk/ops/government_procurement_card/over_£500_GPC_apr_2013.csv')

    # Make assertions
    assert table.sample[0] == [
        'Entity',
        'Transaction Posting Date',
        'Merchant Name',
        'Amount',
        'Description']


def test_web_json_dicts():

    # Get table
    table = topen(BASE_URL % 'data/table-dicts.json')

    # Make assertions
    assert table.headers is None
    assert table.read() == [[1, 'english'], [2, '中国人']]


def test_web_json_lists():

    # Get table
    table = topen(BASE_URL % 'data/table-lists.json')

    # Make assertions
    assert table.headers is None
    assert table.read() == [['id', 'name'], [1, 'english'], [2, '中国人']]


def test_web_excel():

    # Get table
    table = topen(BASE_URL % 'data/table.xls')

    # Make assertions
    assert table.headers is None
    assert table.read() == [['id', 'name'], [1.0, 'english'], [2.0, '中国人']]


def test_native():

    # Get table
    source = [['id', 'name'], ['1', 'english'], ['2', '中国人']]
    table = topen(source)

    # Make assertions
    assert table.headers is None
    assert table.read() == [['id', 'name'], ['1', 'english'], ['2', '中国人']]


def test_native_iterator():

    # Get table
    source = iter([['id', 'name'], ['1', 'english'], ['2', '中国人']])
    table = topen(source)

    # Make assertions
    assert table.headers is None
    assert table.read() == [['id', 'name'], ['1', 'english'], ['2', '中国人']]


def test_native_iterator():

    # Get table
    def generator():
        yield ['id', 'name']
        yield ['1', 'english']
        yield ['2', '中国人']
    with pytest.raises(exceptions.ParsingError) as excinfo:
        iterator = generator()
        topen(iterator)
    assert 'callable' in str(excinfo.value)


def test_native_generator():

    # Get table
    def generator():
        yield ['id', 'name']
        yield ['1', 'english']
        yield ['2', '中国人']
    table = topen(generator)

    # Make assertions
    assert table.headers is None
    assert table.read() == [['id', 'name'], ['1', 'english'], ['2', '中国人']]


def test_native_keyed():

    # Get table
    source = [{'id': '1', 'name': 'english'}, {'id': '2', 'name': '中国人'}]
    table = topen(source, scheme='native', format='native')

    # Make assertions
    assert table.headers is None
    assert table.read() == [['1', 'english'], ['2', '中国人']]


# Tests [headers]

def test_headers():

    # Get table
    table = topen('data/table.csv', headers=1)

    # Make assertions
    assert table.headers == ['id', 'name']
    assert list(table.iter(keyed=True)) == [
        {'id': '1', 'name': 'english'},
        {'id': '2', 'name': '中国人'}]


# DEPRECATED [v0.6-v1)
def test_headers_str():

    # Get table
    table = topen('data/table.csv', headers='row1')

    # Make assertions
    assert table.headers == ['id', 'name']
    assert list(table.iter(keyed=True)) == [
        {'id': '1', 'name': 'english'},
        {'id': '2', 'name': '中国人'}]

def test_headers_user_set():

    # Get table
    source = [['1', 'english'], ['2', '中国人']]
    table = topen(source, headers=['id', 'name'])

    # Make assertions
    assert table.headers == ['id', 'name']
    assert list(table.iter(keyed=True)) == [
        {'id': '1', 'name': 'english'},
        {'id': '2', 'name': '中国人'}]


# DEPRECATED [v0.5-v1)
def test_headers_with_headers_argument():

    # Get table
    table = topen('data/table.csv', with_headers=True)

    # Make assertions
    assert table.headers == ['id', 'name']
    assert list(table.iter(keyed=True)) == [
        {'id': '1', 'name': 'english'},
        {'id': '2', 'name': '中国人'}]


def test_headers_stream_context_manager():

    # Get source
    source = io.open('data/table.csv', mode='rb')

    # Make assertions
    with topen(source, headers='row1', format='csv') as table:
        assert table.headers == ['id', 'name']
        assert table.read(extended=True) == [
            (2, ['id', 'name'], ['1', 'english']),
            (3, ['id', 'name'], ['2', '中国人'])]


def test_headers_native():

    # Get table
    source = [[], ['id', 'name'], ['1', 'english'], ['2', '中国人']]
    table = topen(source, headers='row2')

    # Make assertions
    assert table.headers == ['id', 'name']
    assert table.read(extended=True) == [
        (3, ['id', 'name'], ['1', 'english']),
        (4, ['id', 'name'], ['2', '中国人'])]


def test_headers_json_keyed():

    # Get table
    source = ('text://['
        '{"id": 1, "name": "english"},'
        '{"id": 2, "name": "中国人"}]')
    table = topen(source, headers='row1', format='json')

    # Make assertions
    assert table.headers == ['id', 'name']
    assert list(table.iter(keyed=True)) == [
        {'id': 1, 'name': 'english'},
        {'id': 2, 'name': '中国人'}]


def test_headers_native_keyed():

    # Get table
    source = [{'id': '1', 'name': 'english'}, {'id': '2', 'name': '中国人'}]
    table = topen(source, headers='row1')

    # Make assertions
    assert table.headers == ['id', 'name']
    assert list(table.iter(keyed=True)) == [
        {'id': '1', 'name': 'english'},
        {'id': '2', 'name': '中国人'}]


def test_headers_native_keyed_headers_is_none():

    # Get table
    source = [{'id': '1', 'name': 'english'}, {'id': '2', 'name': '中国人'}]
    table = topen(source, headers=None)

    # Make assertions
    assert table.headers == None
    assert list(table.iter(extended=True)) == [
        (1, None, ['1', 'english']),
        (2, None, ['2', '中国人'])]


# Tests [sample]


def test_sample():

    # Get table
    source = [['id', 'name'], ['1', 'english'], ['2', '中国人']]
    table = topen(source, headers='row1')

    # Make assertions
    assert table.headers == ['id', 'name']
    assert table.sample == [['1', 'english'], ['2', '中国人']]


# Tests [html content]


def test_html_content():

    # Check raises
    source = 'https://github.com/frictionlessdata/tabulator-py/blob/master/data/table.csv'
    with pytest.raises(exceptions.TabulatorException) as excinfo:
        table = topen(source, headers='row1')
    assert 'HTML' in str(excinfo.value)


# Tests [reset]

def test_reset():

    # Get results
    with topen('data/table.csv', headers='row1') as table:
        headers1 = table.headers
        contents1 = table.read()
        table.reset()
        headers2 = table.headers
        contents2 = table.read()

    # Make assertions
    assert headers1 == ['id', 'name']
    assert contents1 == [['1', 'english'], ['2', '中国人']]
    assert headers1 == headers2
    assert contents1 == contents2


def test_reset_and_sample_size():

    # Get table
    table = topen('data/special/long.csv', headers=1, sample_size=3)

    # Make assertions
    assert table.read(extended=True) == [
        (2, ['id', 'name'], ['1', 'a']),
        (3, ['id', 'name'], ['2', 'b']),
        (4, ['id', 'name'], ['3', 'c']),
        (5, ['id', 'name'], ['4', 'd']),
        (6, ['id', 'name'], ['5', 'e']),
        (7, ['id', 'name'], ['6', 'f'])]
    assert table.sample == [['1', 'a'], ['2', 'b']]
    assert table.read() == []

    # Reset table
    table.reset()

    # Make assertions
    assert table.read(extended=True, limit=3) == [
        (2, ['id', 'name'], ['1', 'a']),
        (3, ['id', 'name'], ['2', 'b']),
        (4, ['id', 'name'], ['3', 'c'])]
    assert table.sample == [['1', 'a'], ['2', 'b']]
    assert table.read(extended=True) == [
        (5, ['id', 'name'], ['4', 'd']),
        (6, ['id', 'name'], ['5', 'e']),
        (7, ['id', 'name'], ['6', 'f'])]


def test_reset_generator():

    # Generator
    def generator():
        yield [1]
        yield [2]

    # Get table
    table = topen(generator, sample_size=0)

    # Make assertions
    assert table.read() == [[1], [2]]

    # Reset
    table.reset()

    # Make assertions
    assert table.read() == [[1], [2]]


# Tests [processors]

def test_processors_headers():

    # Processors
    def extract_headers(extended_rows):
        headers = None
        for number, _, row in extended_rows:
            if number == 1:
                headers = row
                continue
            yield (number, headers, row)

    # Get table
    source = [['id', 'name'], ['1', 'english'], ['2', '中国人']]
    table = topen(source, post_parse=[extract_headers])

    # Make assertions
    assert table.headers == None
    assert table.read(extended=True) == [
        (2, ['id', 'name'], ['1', 'english']),
        (3, ['id', 'name'], ['2', '中国人'])]


def test_processors_chain():

    # Processors
    def skip_commented_rows(extended_rows):
        for number, headers, row in extended_rows:
            if (row and hasattr(row[0], 'startswith') and
                    row[0].startswith('#')):
                continue
            yield (number, headers, row)
    def skip_blank_rows(extended_rows):
        for number, headers, row in extended_rows:
            if not row:
                continue
            yield (number, headers, row)
    def cast_rows(extended_rows):
        for number, headers, row in extended_rows:
            crow = []
            for value in row:
                try:
                    if isinstance(value, six.string_types):
                        value = ast.literal_eval(value)
                except Exception:
                    pass
                crow.append(value)
            yield (number, headers, crow)

    # Get table
    source = [['id', 'name'], ['#1', 'english'], [], ['2', '中国人']]
    table = topen(source, headers='row1', post_parse=[
        skip_commented_rows,
        skip_blank_rows,
        cast_rows])

    # Make assertions
    assert table.headers == ['id', 'name']


def test_processors_sample():

    # Processors
    def only_first_row(extended_rows):
        for number, header, row in extended_rows:
            if number == 1:
                yield (number, header, row)

    # Get table
    table = topen('data/table.csv', post_parse=[only_first_row])

    # Make assertions
    assert table.sample == [['id', 'name']]


def test_processors_updating():

    # Processors
    def square(extended_rows):
        for number, header, row in extended_rows:
            yield (number, header, list(map(lambda v: v**2, row)))

    # Get table
    table = topen([[1, 2, 3]])

    # Make assertions
    assert table.sample == [[1, 2, 3]]
    assert table.read() == [[1, 2, 3]]

    # Append processor and reset
    table.post_parse.append(square)
    table.reset()

    # Make assertions
    assert table.sample == [[1, 4, 9]]
    assert table.read() == [[1, 4, 9]]


# Tests [save]

def test_save_csv(tmpdir):

    # Save table
    path = str(tmpdir.join('table.csv'))
    table = topen('data/table.csv', headers=1)
    table.save(path)

    # Open saved table
    table = topen(path, headers=1)

    # Make assertions
    assert table.headers == ['id', 'name']
    assert table.read(extended=True) == [
        (2, ['id', 'name'], ['1', 'english']),
        (3, ['id', 'name'], ['2', '中国人'])]


def test_save_xls(tmpdir):

    # Save table
    path = str(tmpdir.join('table.xls'))
    table = topen('data/table.csv', headers=1)

    # Assert raises
    with pytest.raises(exceptions.WritingError) as excinfo:
        table.save(path)
    assert 'xls' in str(excinfo.value)
