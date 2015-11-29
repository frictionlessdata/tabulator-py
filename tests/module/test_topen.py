import unittest
from importlib import import_module
module = import_module('tabulator.topen')


class topenTest(unittest.TestCase):

    # Tests

    def test(self):
        self.assertTrue(module.topen)
