# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import io
import os
import sys
import pytest
import unittest

from tabulator import topen, processors


FPATH = 'data/%s'
WPATH = 'https://raw.githubusercontent.com/okfn/tabulator-py/master/data/%s'

class Test_topen(unittest.TestCase):

    # Tests [loaders/parsers]

    def test_file_csv(self):

        # Get table
        table = topen(FPATH % 'table.csv')

        # Make assertions
        assert table.headers is None
        assert table.read() == [('id', 'name'), ('1', 'english'), ('2', '中国人')]

    def test_file_json_dicts(self):

        # Get table
        table = topen(FPATH % 'table-dicts.json')

        # Make assertions
        assert table.headers is None
        assert table.read() == [(1, 'english'), (2, '中国人')]

    def test_file_json_lists(self):

        # Get table
        table = topen(FPATH % 'table-lists.json')

        # Make assertions
        assert table.headers is None
        assert table.read() == [('id', 'name'), (1, 'english'), (2, '中国人')]

    def test_file_xls(self):

        # Get table
        table = topen(FPATH % 'table.xls')

        # Make assertions
        assert table.headers is None
        assert table.read() == [('id', 'name'), (1.0, 'english'), (2.0, '中国人')]

    def test_stream_csv(self):

        # Get table
        source = io.open(FPATH % 'table.csv', mode='rb')
        table = topen(source, format='csv')

        # Make assertions
        assert table.headers is None
        assert table.read() == [('id', 'name'), ('1', 'english'), ('2', '中国人')]

    def test_stream_xlsx(self):

        # Get table
        source = io.open(FPATH % 'table.xlsx', mode='rb')
        table = topen(source, format='xlsx')

        # Make assertions
        assert table.headers is None
        assert table.read() == [('id', 'name'), (1.0, 'english'), (2.0, '中国人')]

    def test_text_csv(self):

        # Get table
        source = 'text://id,name\n1,english\n2,中国人\n'
        table = topen(source, format='csv')

        # Make assertions
        assert table.headers is None
        assert table.read() == [('id', 'name'), ('1', 'english'), ('2', '中国人')]

    def test_text_json_dicts(self):

        # Get table
        source = '[{"id": 1, "name": "english" }, {"id": 2, "name": "中国人" }]'
        table = topen(source, scheme='text', format='json')

        # Make assertions
        assert table.headers is None
        assert table.read() == [(1, 'english'), (2, '中国人')]

    def test_text_json_lists(self):

        # Get table
        source = '[["id", "name"], [1, "english"], [2, "中国人"]]'
        table = topen(source, scheme='text', format='json')

        # Make assertions
        assert table.headers is None
        assert table.read() == [('id', 'name'), (1, 'english'), (2, '中国人')]

    def test_web_csv(self):

        # Get table
        table = topen(WPATH % 'table.csv')

        # Make assertions
        assert table.headers is None
        assert table.read() == [('id', 'name'), ('1', 'english'), ('2', '中国人')]

    def test_web_json_dicts(self):

        # Get table
        table = topen(WPATH % 'table-dicts.json')

        # Make assertions
        assert table.headers is None
        assert table.read() == [(1, 'english'), (2, '中国人')]

    def test_web_json_lists(self):

        # Get table
        table = topen(WPATH % 'table-lists.json')

        # Make assertions
        assert table.headers is None
        assert table.read() == [('id', 'name'), (1, 'english'), (2, '中国人')]

    def test_web_excel(self):

        # Get table
        table = topen(WPATH % 'table.xls')

        # Make assertions
        assert table.headers is None
        assert table.read() == [('id', 'name'), (1.0, 'english'), (2.0, '中国人')]

    def test_native(self):

        # Get table
        source = [['id', 'name'], ['1', 'english'], ('2', '中国人')]
        table = topen(source)

        # Make assertions
        assert table.headers is None
        assert table.read() == [('id', 'name'), ('1', 'english'), ('2', '中国人')]

    def test_native_iterator(self):

        # Get table
        source = iter([['id', 'name'], ['1', 'english'], ('2', '中国人')])
        table = topen(source)

        # Make assertions
        assert table.headers is None
        assert table.read() == [('id', 'name'), ('1', 'english'), ('2', '中国人')]

    def test_native_generator(self):

        # Get table
        def generator():
            yield ['id', 'name']
            yield ['1', 'english']
            yield ('2', '中国人')
        source = generator()
        table = topen(source)

        # Make assertions
        assert table.headers is None
        assert table.read() == [('id', 'name'), ('1', 'english'), ('2', '中国人')]

    def test_native_keyed(self):

        # Get table
        source = [{'id': '1', 'name': 'english'}, {'id': '2', 'name': '中国人'}]
        table = topen(source, scheme='native', format='native')

        # Make assertions
        assert table.headers is None
        assert table.read() == [('1', 'english'), ('2', '中国人')]

    # Tests [processors]

    def test_headers(self):

        # Get table
        table = topen(FPATH % 'table.csv', with_headers=True)

        # Make assertions
        assert table.headers == ('id', 'name')
        assert list(table.iter(keyed=True)) == [
            {'id': '1', 'name': 'english'},
            {'id': '2', 'name': '中国人'}]

    def test_headers_via_processors_param(self):

        # Get results
        table = topen(FPATH % 'table.csv', with_headers=True,
            processors=[processors.Headers()])

        # Make assertions
        assert table.headers == ('id', 'name')
        assert list(table.iter(keyed=True)) == [
            {'id': '1', 'name': 'english'},
            {'id': '2', 'name': '中国人'}]

    def test_headers_json(self):

        # Get table
        source = ('text://['
            '{"id": 1, "name": "english"},'
            '{"id": 2, "value": "中国人"}]')
        table = topen(source, with_headers=True, format='json')

        # Make assertions
        assert table.headers == ('id', 'name')
        assert list(table.iter(keyed=True)) == [
            {'id': 1, 'name': 'english'},
            {'id': 2, 'name': '中国人'}]

    def test_headers_native(self):

        # Get table
        source = [{'id': '1', 'name': 'english'}, {'id': '2', 'name': '中国人'}]
        table = topen(source, with_headers=True)

        # Make assertions
        assert table.headers == ('id', 'name')
        assert table.read() == [('1', 'english'), ('2', '中国人')]

    def test_headers_iter_keyed(self):

        # Get table
        source = [['id', 'name'], ['1', 'english'], ('2', '中国人')]
        table = topen(source, with_headers=True)

        # Make assertions
        assert table.headers == ('id', 'name')
        assert list(table.iter(keyed=True)) == [
            {'id': '1', 'name': 'english'},
            {'id': '2', 'name': '中国人'}]

    # It works for Python 2 but values convertion differs
    @pytest.mark.skipif(sys.version_info < (3,3), reason='requires python 3.3')
    def test_convert(self):

        # Get table
        table = topen(FPATH % 'table.csv',
            with_headers=True, processors=[processors.Convert()])

        # Make assertions
        assert table.headers == ('id', 'name')
        assert table.read() == [(1, 'english'), (2, '中国人')]

    def test_convert_custom(self):

        # Get table
        def converter(values):
            return [float(values[0]), values[1]]
        table = topen(FPATH % 'table.csv',
            with_headers=True, processors=[processors.Convert(converter)])

        # Make assertions
        assert table.headers == ('id', 'name')
        assert table.read() == [(1.0, 'english'), (2.0, '中国人')]

    # Tests [reset]

    def test_reset(self):

        # Get results
        with topen(FPATH % 'table.csv', with_headers=True) as table:
            headers1 = table.headers
            contents1 = table.read()
            table.reset()
            headers2 = table.headers
            contents2 = table.read()

        # Make assertions
        assert headers1 == ('id', 'name')
        assert contents1 == [('1', 'english'), ('2', '中国人')]
        assert headers1 == headers2
        assert contents1 == contents2
