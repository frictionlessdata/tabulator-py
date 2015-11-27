# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import csv
from .api import API


class CSV(API):
    """Parser to parse CSV data format.
    """

    # Public

    def __init__(self, **options):
        self.__options = options
        self.__loader = None
        self.__chars = None
        self.__items = None

    def open(self, loader):
        self.close()
        self.__loader = loader
        self.__chars = loader.load(mode='t')
        items = csv.reader(self.__chars, **self.__options)
        self.__items = ((None, tuple(line)) for line in items)

    def close(self):
        if not self.closed:
            self.__chars.close()

    @property
    def closed(self):
        return self.__chars is None or self.__chars.closed

    @property
    def items(self):
        return self.__items

    def reset(self):
        if not self.__chars.seekable():
            message = (
                'Loader\'s returned not seekable stream. '
                'For this stream reset is not supported.')
            raise RuntimeError(message)
        self.__chars.seek(0)
