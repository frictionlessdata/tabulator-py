# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import csv
import six
from codecs import iterencode
from .. import helpers
from . import api


# Module API

class CSVParser(api.Parser):
    """Parser to parse CSV data format.
    """

    # Public

    def __init__(self, **options):
        self.__extended_rows = None
        self.__options = options
        self.__loader = None
        self.__chars = None

    @property
    def closed(self):
        return self.__chars is None or self.__chars.closed

    def open(self, source, encoding, loader):
        self.close()
        self.__loader = loader
        self.__chars = loader.load(source, encoding, mode='t')
        self.reset()

    def close(self):
        if not self.closed:
            self.__chars.close()

    def reset(self):
        helpers.reset_stream(self.__chars)
        self.__extended_rows = self.__iter_extended_rows()

    @property
    def extended_rows(self):
        return self.__extended_rows

    # Private

    def __iter_extended_rows(self):

        # For PY2 encode/decode
        if six.PY2:
            # Reader requires utf-8 encoded stream
            bytes = iterencode(self.__chars, 'utf-8')
            items = csv.reader(bytes, **self.__options)
            for number, item in enumerate(items, start=1):
                values = []
                for value in item:
                    value = value.decode('utf-8')
                    values.append(value)
                yield (number, None, list(values))

        # For PY3 use chars
        else:
            items = csv.reader(self.__chars, **self.__options)
            for number, item in enumerate(items, start=1):
                yield (number, None, list(item))
