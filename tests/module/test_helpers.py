import unittest
from importlib import import_module
module = import_module('tabulator.helpers')


class helpersTest(unittest.TestCase):

    # Tests

    def test(self):
        self.assertTrue(module)
