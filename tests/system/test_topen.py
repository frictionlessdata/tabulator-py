# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import os
import unittest
from tabulator import topen, processors


class topenTest(unittest.TestCase):

    # Helpers

    def make_file_path(self, *paths):
        basedir = os.path.join(os.path.dirname(__file__), '..', '..')
        return os.path.join(basedir, 'examples', 'data', *paths)

    def make_web_path(self, *paths):
        baseurl = 'https://raw.githubusercontent.com'
        baseurl += '/okfn/tabulator-py/master/examples/data'
        return '/'.join([baseurl] + list(paths))

    # Tests [loaders/parsers]

    def test_file_csv(self):

        # Get results
        actual = topen(self.make_file_path('table.csv')).read()
        expected = [('id', 'name'), ('1', 'english'), ('2', '中国人')]

        # Make assertions
        self.assertEqual(actual, expected)

    def test_file_json_dicts(self):

        # Get results
        actual = topen(self.make_file_path('table-dicts.json')).read()
        expected = [(1, 'english'), (2, '中国人')]

        # Make assertions
        self.assertEqual(actual, expected)

    def test_file_json_lists(self):

        # Get results
        actual = topen(self.make_file_path('table-lists.json')).read()
        expected = [('id', 'name'), (1, 'english'), (2, '中国人')]

        # Make assertions
        self.assertEqual(actual, expected)

    def test_file_excel(self):

        # Get results
        actual = topen(self.make_file_path('table.xls')).read()
        expected = [('id', 'name'), (1.0, 'english'), (2.0, '中国人')]

        # Make assertions
        self.assertEqual(actual, expected)

    def test_text_csv(self):

        # Get results
        source = 'id,name\n1,english\n2,中国人\n'
        actual = topen(source, scheme='text', format='csv').read()
        expected = [('id', 'name'), ('1', 'english'), ('2', '中国人')]

        # Make assertions
        self.assertEqual(actual, expected)

    def test_text_json_dicts(self):

        # Get results
        source = '[{"id": 1, "name": "english" }, {"id": 2, "name": "中国人" }]'
        actual = topen(source, scheme='text', format='json').read()
        expected = [(1, 'english'), (2, '中国人')]

        # Make assertions
        self.assertEqual(actual, expected)

    def test_text_json_lists(self):

        # Get results
        source = '[["id", "name"], [1, "english"], [2, "中国人"]]'
        actual = topen(source, scheme='text', format='json').read()
        expected = [('id', 'name'), (1, 'english'), (2, '中国人')]

        # Make assertions
        self.assertEqual(actual, expected)

    def test_web_csv(self):

        # Get results
        actual = topen(self.make_web_path('table.csv')).read()
        expected = [('id', 'name'), ('1', 'english'), ('2', '中国人')]

        # Make assertions
        self.assertEqual(actual, expected)

    def test_web_json_dicts(self):

        # Get results
        actual = topen(self.make_web_path('table-dicts.json')).read()
        expected = [(1, 'english'), (2, '中国人')]

        # Make assertions
        self.assertEqual(actual, expected)

    def test_web_json_lists(self):

        # Get results
        actual = topen(self.make_web_path('table-lists.json')).read()
        expected = [('id', 'name'), (1, 'english'), (2, '中国人')]

        # Make assertions
        self.assertEqual(actual, expected)

    def test_web_excel(self):

        # Get results
        actual = topen(self.make_web_path('table.xls')).read()
        expected = [('id', 'name'), (1.0, 'english'), (2.0, '中国人')]

        # Make assertions
        self.assertEqual(actual, expected)

    # Tests [processors]

    def test_headers(self):

        # Get results
        with topen(self.make_file_path('table.csv')) as table:
            table.add_processor(processors.Headers())
            headers = table.headers
            contents = table.read(with_headers=True)

        # Make assertions
        self.assertEqual(headers, ('id', 'name'))
        self.assertEqual(contents, [('1', 'english'), ('2', '中国人')])
        self.assertEqual(contents[0].id, '1')
        self.assertEqual(contents[0].name, 'english')

    # Tests [reset]

    def test_reset(self):

        # Get results
        with topen(self.make_file_path('table.csv')) as table:
            table.add_processor(processors.Headers())
            contents1 = table.read(with_headers=True)
            table.reset()
            contents2 = table.read(with_headers=True)

        # Make assertions
        self.assertEqual(contents1, [('1', 'english'), ('2', '中国人')])
        self.assertEqual(contents2, [('1', 'english'), ('2', '中国人')])
