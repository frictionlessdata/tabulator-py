# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import csv
import six
from codecs import iterencode
from .. import errors
from .. import helpers
from . import api


# Module API

class NativeParser(api.Parser):
    """Parser to provide support for python native lists.
    """

    # Public

    def __init__(self, **options):
        self.__options = options
        self.__loader = None
        self.__items = None

    def open(self, loader):
        self.close()
        self.__loader = loader
        self.reset()

    def close(self):
        pass

    @property
    def closed(self):
        return False

    @property
    def items(self):
        return self.__items

    def reset(self):
        self.__items = self.__emit_items()

    # Private

    def __emit_items(self):
        items = self.__loader.source
        for item in items:
            if isinstance(item, list):
                yield (None, tuple(item))
            elif isinstance(item, dict):
                keys = []
                values = []
                for key in sorted(item.keys()):
                    keys.append(key)
                    values.append(item[key])
                yield (tuple(keys), tuple(values))
            else:
                raise errors.Error('Native item has to be list or dict')
