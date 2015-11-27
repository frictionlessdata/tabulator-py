# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import os
import unittest
from tabulator import topen


class topenTest(unittest.TestCase):

    # Helpers

    def make_file_path(self, *paths):
        basedir = os.path.join(os.path.dirname(__file__), '..', '..')
        return os.path.join(basedir, 'examples', 'data', *paths)

    def make_web_path(self, *paths):
        baseurl = 'https://raw.githubusercontent.com'
        basepath = 'okfn/tabulator-py/master/examples/data'
        return '/'.join([baseurl, basepath] + list(paths))

    # Tests

    def test_file_csv(self):

        # Get results
        actual = topen(self.make_file_path('table.csv')).read()
        expected = [('id', 'name'), ('1', 'name1'), ('2', 'name2')]

        # Make assertions
        self.assertEqual(actual, expected)

    def test_file_json(self):

        # Get results
        actual = topen(self.make_file_path('table.json')).read()
        expected = [(1, 'name1'), (2, 'name2')]

        # Make assertions
        self.assertEqual(actual, expected)

    def test_file_excel(self):

        # Get results
        actual = topen(self.make_file_path('table.xls')).read()
        expected = [('id', 'name'), (1.0, 'name1'), (2.0, 'name2')]

        # Make assertions
        self.assertEqual(actual, expected)

    def test_text_csv(self):

        # Get results
        source = 'id,name\n1,name1\n2,name2\n'
        actual = topen(source, scheme='text', format='csv').read()
        expected = [('id', 'name'), ('1', 'name1'), ('2', 'name2')]

        # Make assertions
        self.assertEqual(actual, expected)

    def test_text_json(self):

        # Get results
        source = '[{"id": 1, "name": "name1" }, {"id": 2, "name": "name2" }]'
        actual = topen(source, scheme='text', format='json').read()
        expected = [(1, 'name1'), (2, 'name2')]

        # Make assertions
        self.assertEqual(actual, expected)

    def test_web_csv(self):

        # Get results
        actual = topen(self.make_web_path('table.csv')).read()
        expected = [('id', 'name'), ('1', 'name1'), ('2', 'name2')]

        # Make assertions
        self.assertEqual(actual, expected)

    def test_web_json(self):

        # Get results
        actual = topen(self.make_web_path('table.json')).read()
        expected = [(1, 'name1'), (2, 'name2')]

        # Make assertions
        self.assertEqual(actual, expected)

    def test_web_excel(self):

        # Get results
        actual = topen(self.make_web_path('table.xls')).read()
        expected = [('id', 'name'), (1.0, 'name1'), (2.0, 'name2')]

        # Make assertions
        self.assertEqual(actual, expected)
