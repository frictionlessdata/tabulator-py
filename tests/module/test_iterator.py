import unittest
from importlib import import_module
module = import_module('tabulator.iterator')


class IteratorTest(unittest.TestCase):

    # Tests

    def test(self):
        self.assertTrue(module.Iterator)
