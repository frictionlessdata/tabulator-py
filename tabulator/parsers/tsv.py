# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import tsv
from .. import helpers
from . import api


# Module API

class TSVParser(api.Parser):
    """Parser to parse linear TSV data format.

    See: http://dataprotocols.org/linear-tsv/

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
        items = tsv.un(self.__chars)
        for number, item in enumerate(items, start=1):
            yield (number, None, list(item))
