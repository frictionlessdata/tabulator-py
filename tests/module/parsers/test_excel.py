# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import unittest
from importlib import import_module
module = import_module('tabulator.parsers.excel')

import os
import unittest
try:
    from unittest.mock import Mock
except ImportError:
    from mock import Mock
from importlib import import_module
module = import_module('tabulator.parsers.excel')


class ExcelTest(unittest.TestCase):

    # Actions

    def setUp(self):
        basedir = os.path.join(os.path.dirname(__file__), '..', '..', '..')
        self.source = os.path.join(basedir, 'examples', 'data', 'table.xls')
        self.loader = Mock()
        self.loader.load = Mock(return_value=open(self.source, 'rb'))
        self.parser = module.Excel()

    # Tests

    def test(self):

        self.assertTrue(self.parser.closed)
        self.parser.open(self.loader)
        self.assertFalse(self.parser.closed)

        self.assertEqual(
            list(self.parser.items),
            [(None, ('id', 'name')),
                (None, (1.0, 'name1')),
                (None, (2.0, 'name2'))])

        self.assertEqual(len(list(self.parser.items)), 0)
        self.parser.reset()
        self.assertEqual(len(list(self.parser.items)), 3)

        self.parser.close()
        self.assertTrue(self.parser.closed)
