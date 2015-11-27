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


    def make_path(self, *paths):
        return os.path.join(
            os.path.dirname(__file__), '..', '..', 'examples', 'data', *paths)

    # Tests

    def test_file_csv(self):
        actual = topen(self.make_path('table.csv')).read()
        expected = [('id', 'name'), ('1', 'name1'), ('2', 'name2')]
        self.assertEqual(actual, expected)

    def test_file_json(self):
        actual = topen(self.make_path('table.json')).read()
        expected = [(1, 'name1'), (2, 'name2')]
        self.assertEqual(actual, expected)

    def test_file_excel(self):
        actual = topen(self.make_path('table.xls')).read()
        expected = [('id', 'name'), (1.0, 'name1'), (2.0, 'name2')]
        self.assertEqual(actual, expected)
