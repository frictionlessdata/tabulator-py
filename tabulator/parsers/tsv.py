# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import tsv
from ..parser import Parser
from .. import helpers


# Module API

class TSVParser(Parser):
    """Parser to parse linear TSV data format.

    See: http://dataprotocols.org/linear-tsv/

    """

    # Public

    options = []

    def __init__(self, loader):
        self.__loader = loader
        self.__force_parse = None
        self.__extended_rows = None
        self.__chars = None

    @property
    def closed(self):
        return self.__chars is None or self.__chars.closed

    def open(self, source, encoding=None, force_parse=False):
        self.close()
        self.__force_parse = force_parse
        self.__chars = self.__loader.load(source, encoding=encoding)
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
        for row_number, item in enumerate(items, start=1):
            yield (row_number, None, list(item))
