# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import unittest
from importlib import import_module
module = import_module('tabulator.helpers')


class helpersTest(unittest.TestCase):

    # Tests

    def test_detect_scheme(self):
        self.assertTrue(module.detect_scheme)

    def test_detect_format(self):
        self.assertTrue(module.detect_format)

    def test_detect_encoding(self):
        self.assertTrue(module.detect_encoding)

    def test_reset_stream(self):
        self.assertTrue(module.reset_stream)
