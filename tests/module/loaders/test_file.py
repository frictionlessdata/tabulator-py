import unittest
from importlib import import_module
module = import_module('tabulator.loaders.file')


class FileTest(unittest.TestCase):

    # Tests

    def test(self):
        self.assertTrue(module.File)
