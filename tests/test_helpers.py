# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import io
import os
import unittest
from tabulator import helpers


class Test_detect_scheme(unittest.TestCase):

    # Tests

    def test(self):
        self.assertEqual(helpers.detect_scheme('text://path'), 'text')
        self.assertEqual(helpers.detect_scheme('stream://path'), 'stream')
        self.assertEqual(helpers.detect_scheme('file://path'), 'file')
        self.assertEqual(helpers.detect_scheme('ftp://path'), 'ftp')
        self.assertEqual(helpers.detect_scheme('ftps://path'), 'ftps')
        self.assertEqual(helpers.detect_scheme('http://path'), 'http')
        self.assertEqual(helpers.detect_scheme('https://path'), 'https')
        self.assertEqual(helpers.detect_scheme('xxx://path'), 'xxx')
        self.assertEqual(helpers.detect_scheme('xx://path'), 'xx')
        self.assertEqual(helpers.detect_scheme('XXX://path'), 'xxx')
        self.assertEqual(helpers.detect_scheme('XX://path'), 'xx')
        self.assertEqual(helpers.detect_scheme('c://path'), None)
        self.assertEqual(helpers.detect_scheme('c:\\path'), None)
        self.assertEqual(helpers.detect_scheme('c:\path'), None)
        self.assertEqual(helpers.detect_scheme('http:/path'), None)
        self.assertEqual(helpers.detect_scheme('http//path'), None)
        self.assertEqual(helpers.detect_scheme('path'), None)


class Test_detect_format(unittest.TestCase):

    # Tests

    def test(self):
        self.assertEqual(helpers.detect_format('path.CsV'), 'csv')

    def test_works_with_urls_with_query_and_fragment_components(self):
        url = 'http://someplace.com/foo/path.csv?foo=bar#baz'
        self.assertEqual(helpers.detect_format(url), 'csv')


class Test_detect_encoding(unittest.TestCase):

    # Tests

    def test(self):
        path = os.path.join(os.path.dirname(__file__), '..', 'README.md')
        bytes = io.open(path, 'rb')
        self.assertEqual(helpers.detect_encoding(bytes), 'utf-8')

    def test_unknown(self):
        bytes = io.BytesIO(b'\xff\x81')
        self.assertEqual(helpers.detect_encoding(bytes), 'utf-8')

    def test_long(self):
        bytes = io.BytesIO(b'A\n' * 1000 + b'\xff\xff')
        self.assertEqual(helpers.detect_encoding(bytes), 'utf-8')

    def test_not_so_long(self):
        bytes = io.BytesIO(b'A\n' * 999 + b'\xff\xff')
        self.assertEqual(helpers.detect_encoding(bytes), 'windows-1252')


class Test_reset_stream(unittest.TestCase):

    # Tests

    def test_seekable(self):
        file = io.open(__file__)
        file.seek(1)
        self.assertEqual(file.tell(), 1)
        helpers.reset_stream(file)
        self.assertEqual(file.tell(), 0)

    def test_not_seekable(self):
        self.assertRaises(Exception, helpers.reset_stream, 'not_seekable')
