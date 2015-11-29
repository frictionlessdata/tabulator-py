import unittest
from importlib import import_module
module = import_module('tabulator.loaders.web')


class WebTest(unittest.TestCase):

    # Tests

    def test(self):
        self.assertTrue(module.Web)
