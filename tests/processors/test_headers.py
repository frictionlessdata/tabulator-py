# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import unittest

from tabulator import processors


class TestHeaders(unittest.TestCase):

    # Tests

    def test(self):
        self.assertTrue(processors.Headers)
