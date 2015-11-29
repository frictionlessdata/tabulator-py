import unittest
from importlib import import_module
module = import_module('tabulator.loaders.text')


class TextTest(unittest.TestCase):

    # Tests

    def test(self):
        self.assertTrue(module.Text)
