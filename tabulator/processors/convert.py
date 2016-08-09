# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import ast
from .. import helpers
from . import api


# Module API

class ConvertProcessor(api.Processor):
    """Processor to convert row values.

    If converter is not passed row values will be converted
    using python literal parser (ast.literal_eval).

    Args:
        converter (callable): callable with signature converter(values) -> values

    """

    # Public

    def __init__(self, converter=None):
        if converter is None:
            converter = _convert
        self.__converter = converter

    def process(self, iterator):
        iterator.values = tuple(self.__converter(iterator.values))

    def handle(self, iterator):
        pass  # pragma: no cover


# Internal

def _convert(values):
    """Convert values to python objects.
    """
    converted_values = []
    for value in values:
        try:
            if isinstance(value, str):
                value = ast.literal_eval(value)
        except Exception:
            pass
        converted_values.append(value)
    return converted_values
