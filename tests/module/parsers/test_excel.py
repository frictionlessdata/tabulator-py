import unittest
from importlib import import_module
module = import_module('tabulator.parsers.excel')


class ExcelTest(unittest.TestCase):

    # Tests

    def test(self):
        self.assertTrue(module.Excel)
