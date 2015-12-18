# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import os
import unittest
from importlib import import_module
module = import_module('tabulator.loaders.file')


class TestFile(unittest.TestCase):

    # Actions

    def setUp(self):
        basedir = os.path.join(os.path.dirname(__file__), '..', '..', '..')
        self.source = os.path.join(basedir, 'examples', 'data', 'table.csv')
        self.encoding = 'utf-8'
        self.loader = module.File(self.source, self.encoding)

    # Tests

    def test_load_t(self):
        chars = self.loader.load(mode='t')
        self.assertEqual(chars.read(), 'id,name\n1,english\n2,中国人\n')

    def test_load_b(self):
        spec = '中国人'.encode('utf-8')
        chars = self.loader.load(mode='b')
        self.assertEqual(chars.read(), b'id,name\n1,english\n2,' + spec + b'\n')

    def test_encoding(self):
        self.assertEqual(self.loader.encoding, self.encoding)
