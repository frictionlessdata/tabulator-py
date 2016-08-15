# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import io
import sys
import pytest
from tabulator import topen, parsers, processors


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


def test_native_generator():

    # Get table
    def generator():
        yield ['id', 'name']
        yield ['1', 'english']
        yield ['2', '中国人']
    source = generator()
    table = topen(source)

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


# Tests [sample]


def test_sample():

    # Get table
    source = [['id', 'name'], ['1', 'english'], ['2', '中国人']]
    table = topen(source, headers='row1')

    # Make assertions
    assert table.headers == ['id', 'name']
    assert table.sample == [
        (2, None, ['1', 'english']),
        (3, None, ['2', '中国人'])]


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


# Tests [processors]


def test_processors_chain():

    # Get table
    source = [['id', 'name'], ['#1', 'english'], [], ['2', '中国人']]
    table = topen(source, headers='row1', post_parse=[
        processors.skip_commented_rows,
        processors.skip_blank_rows,
        processors.convert_rows])

    # Make assertions
    assert table.headers == ['id', 'name']
    assert table.read() == [[2, '中国人']]
