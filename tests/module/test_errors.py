import unittest
from importlib import import_module
module = import_module('tabulator.errors')


class errorsTest(unittest.TestCase):

    # Tests

    def test(self):
        self.assertTrue(module)
