# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import unittest
try:
    from unittest.mock import Mock, patch
except ImportError:
    from mock import Mock, patch
from importlib import import_module
module = import_module('tabulator.topen')


class topenTest(unittest.TestCase):

    # Actions

    def setUp(self):
        self.addCleanup(patch.stopall)
        self.Table = patch.object(module, 'Table').start()
        self.Loader = Mock()
        self.Parser = Mock()
        self.encoding = 'encoding'

    # Tests

    def test_supported_in_source(self):
        for scheme in ['file', 'text', 'ftp', 'ftps', 'http', 'https']:
            for format in ['csv', 'xls', 'xlsx', 'json']:
                patch.object(module, 'LOADERS', {scheme: self.Loader}).start()
                patch.object(module, 'PARSERS', {format: self.Parser}).start()
                source = '%s://path.%s' % (scheme, format)
                table = module.topen(source, encoding=self.encoding)
                self.assertEqual(table, self.Table.return_value)
                self.Loader.assert_called_with(source, self.encoding)
                self.Parser.assert_called_with()
                self.Table.assert_called_with(
                        loader=self.Loader(),
                        parser=self.Parser())

    def test_supported_in_parameters(self):
        for scheme in ['file', 'text', 'ftp', 'ftps', 'http', 'https']:
            for format in ['csv', 'xls', 'xlsx', 'json']:
                patch.object(module, 'LOADERS', {scheme: self.Loader}).start()
                patch.object(module, 'PARSERS', {format: self.Parser}).start()
                source = 'path'
                table = module.topen(
                        source,
                        scheme=scheme,
                        format=format,
                        encoding=self.encoding)
                self.assertEqual(table, self.Table.return_value)
                self.Loader.assert_called_with(source, self.encoding)
                self.Parser.assert_called_with()
                self.Table.assert_called_with(
                        loader=self.Loader(),
                        parser=self.Parser())

    def test_not_supported(self):
        self.assertRaises(Exception, module.topen, 'path',
                scheme='not_supported', format='csv')
        self.assertRaises(Exception, module.topen, 'path',
                scheme='file', format='not_supported')
