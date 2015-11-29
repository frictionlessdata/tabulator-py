import unittest
from importlib import import_module
module = import_module('tabulator.parsers.csv')


class CSVTest(unittest.TestCase):

    # Tests

    def test(self):
        self.assertTrue(module.CSV)
