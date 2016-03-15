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


class Test_detect_scheme(unittest.TestCase):

    # Tests

    def test(self):
        self.assertEqual(module.detect_scheme('text://path'), 'text')
        self.assertEqual(module.detect_scheme('stream://path'), 'stream')
        self.assertEqual(module.detect_scheme('file://path'), 'file')
        self.assertEqual(module.detect_scheme('ftp://path'), 'ftp')
        self.assertEqual(module.detect_scheme('ftps://path'), 'ftps')
        self.assertEqual(module.detect_scheme('http://path'), 'http')
        self.assertEqual(module.detect_scheme('https://path'), 'https')
        self.assertEqual(module.detect_scheme('xxx://path'), 'xxx')
        self.assertEqual(module.detect_scheme('xx://path'), 'xx')
        self.assertEqual(module.detect_scheme('XXX://path'), 'xxx')
        self.assertEqual(module.detect_scheme('XX://path'), 'xx')
        self.assertEqual(module.detect_scheme('c://path'), None)
        self.assertEqual(module.detect_scheme('c:\\path'), None)
        self.assertEqual(module.detect_scheme('c:\path'), None)
        self.assertEqual(module.detect_scheme('http:/path'), None)
        self.assertEqual(module.detect_scheme('http//path'), None)
        self.assertEqual(module.detect_scheme('path'), None)


class Test_detect_format(unittest.TestCase):

    # Tests

    def test(self):
        self.assertEqual(module.detect_format('path.CsV'), 'csv')

    def test_works_with_urls_with_query_and_fragment_components(self):
        url = 'http://someplace.com/foo/path.csv?foo=bar#baz'
        self.assertEqual(module.detect_format(url), 'csv')


class Test_detect_encoding(unittest.TestCase):

    # Tests

    def test(self):
        path = os.path.join(os.path.dirname(__file__), '..', '..', 'README.md')
        bytes = io.open(path, 'rb')
        self.assertEqual(module.detect_encoding(bytes), 'utf-8')


class Test_reset_stream(unittest.TestCase):

    # Tests

    def test_seekable(self):
        file = io.open(__file__)
        file.seek(1)
        self.assertEqual(file.tell(), 1)
        module.reset_stream(file)
        self.assertEqual(file.tell(), 0)

    def test_not_seekable(self):
        self.assertRaises(Exception, module.reset_stream, 'not_seekable')
