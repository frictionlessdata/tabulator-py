# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import unittest
from tabulator import loaders


class TestText(unittest.TestCase):

    # Actions

    def setUp(self):
        self.source = 'id,name\n1,english\n2,中国人\n'
        self.encoding = 'utf-8'
        self.loader = loaders.Text()

    # Tests

    def test_load_t(self):
        chars = self.loader.load(self.source, self.encoding, mode='t')
        self.assertEqual(chars.read(), 'id,name\n1,english\n2,中国人\n')

    def test_load_b(self):
        spec = '中国人'.encode('utf-8')
        chars = self.loader.load(self.source, self.encoding, mode='b')
        self.assertEqual(chars.read(), b'id,name\n1,english\n2,' + spec + b'\n')
