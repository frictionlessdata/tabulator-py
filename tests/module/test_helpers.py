# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import io
import os
import unittest
from importlib import import_module
module = import_module('tabulator.helpers')


class detect_schemeTest(unittest.TestCase):

    # Tests

    def test(self):
        self.assertEqual(module.detect_scheme('http://path'), 'http')


class detect_formatTest(unittest.TestCase):

    # Tests

    def test(self):
        self.assertEqual(module.detect_format('path.csv'), 'csv')


class detect_encoding(unittest.TestCase):

    # Tests

    def test(self):
        path = os.path.join(os.path.dirname(__file__), '..', '..', 'README.md')
        bytes = io.open(path, 'rb')
        self.assertEqual(module.detect_encoding(bytes), 'utf-8')


class reset_streamTest(unittest.TestCase):

    # Tests

    def test_seekable(self):
        file = io.open(__file__)
        file.seek(1)
        self.assertEqual(file.tell(), 1)
        module.reset_stream(file)
        self.assertEqual(file.tell(), 0)

    def test_not_seekable(self):
        self.assertRaises(Exception, module.reset_stream, 'not_seekable')
