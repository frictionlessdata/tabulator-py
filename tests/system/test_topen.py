# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import io
import os
import unittest
from tabulator import topen, processors


FPATH = 'examples/data/%s'
WPATH = 'https://raw.githubusercontent.com/okfn/tabulator-py/master/examples/data/%s'

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

    # Tests [processors]

    def test_headers(self):

        # Get results
        with topen(FPATH % 'table.csv', with_headers=True) as table:
            headers = table.headers
            contents = table.read()

        # Make assertions
        assert headers == ('id', 'name')
        assert contents == [('1', 'english'), ('2', '中国人')]
        assert contents[0].get('id') == '1'
        assert contents[0].get('name') == 'english'
        assert contents[1].get('id') == '2'
        assert contents[1].get('name') == '中国人'

    def test_headers_via_processors_param(self):

        # Get results
        with topen(FPATH % 'table.csv',
                   with_headers=True,
                   processors=[processors.Headers()]) as table:
            headers = table.headers
            contents = table.read()

        # Make assertions
        assert headers == ('id', 'name')
        assert contents == [('1', 'english'), ('2', '中国人')]
        assert contents[0].get('id') == '1'
        assert contents[0].get('name') == 'english'
        assert contents[1].get('id') == '2'
        assert contents[1].get('name') == '中国人'

    def test_headers_json(self):

        # Get results
        source = ('text://['
            '{"country": "China", "value": "中国"},'
            '{"country": "Brazil", "value": "Brazil"}]')
        with topen(source, with_headers=True, format='json') as table:
            headers = table.headers
            contents = table.read()

        # Make assertions
        assert headers == ('country', 'value')
        assert contents == [('China', '中国'), ('Brazil', 'Brazil')]
        assert contents[0].get('country') == 'China'
        assert contents[0].get('value') == '中国'
        assert contents[1].get('country') == 'Brazil'
        assert contents[1].get('value') == 'Brazil'

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
