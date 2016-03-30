# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import unittest

from tabulator import errors


class Test_errors(unittest.TestCase):

    # Tests

    def test(self):
        self.assertTrue(issubclass(errors.Error, Exception))
