# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import unittest
from importlib import import_module
module = import_module('tabulator.processors.schema')


class TestSchema(unittest.TestCase):

    # Tests

    def test(self):
        self.assertTrue(module.Schema)
