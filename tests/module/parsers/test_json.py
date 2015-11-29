import unittest
from importlib import import_module
module = import_module('tabulator.parsers.json')


class JSONTest(unittest.TestCase):

    # Tests

    def test(self):
        self.assertTrue(module.JSON)
