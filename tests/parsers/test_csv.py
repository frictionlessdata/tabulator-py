# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import io
import os
import unittest
from mock import Mock

from tabulator import parsers


class TestCSV(unittest.TestCase):

    # Actions

    def setUp(self):
        basedir = os.path.join(os.path.dirname(__file__), '..', '..')
        self.source = os.path.join(basedir, 'data', 'table.csv')
        self.loader = Mock()
        self.loader.load = Mock(return_value=io.open(self.source, encoding='utf-8'))
        self.parser = parsers.CSV()

    # Tests

    def test(self):

        self.assertTrue(self.parser.closed)
        self.parser.open(self.loader)
        self.assertFalse(self.parser.closed)

        self.assertEqual(
            list(self.parser.items),
            [(None, ('id', 'name')),
                (None, ('1', 'english')),
                (None, ('2', '中国人'))])

        self.assertEqual(len(list(self.parser.items)), 0)
        self.parser.reset()
        self.assertEqual(len(list(self.parser.items)), 3)

        self.parser.close()
        self.assertTrue(self.parser.closed)
