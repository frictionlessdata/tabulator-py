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
        self.__options = options
        self.__loader = None
        self.__chars = None
        self.__items = None

    def open(self, loader):
        self.close()
        self.__loader = loader
        self.__chars = loader.load(mode='t')
        self.reset()

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
        helpers.reset_stream(self.__chars)
        self.__items = self.__emit_items()

    # Private

    def __emit_items(self):
        items = tsv.un(self.__chars)
        for item in items:
            yield (None, tuple(item))
