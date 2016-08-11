# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

from .. import errors
from . import api


# Module API

class NativeParser(api.Parser):
    """Parser to provide support for python native lists.
    """

    # Public

    def __init__(self, **options):
        self.__options = options
        self.__source = None
        self.__items = None

    @property
    def closed(self):
        return False

    def open(self, source, encoding, loader):
        self.close()
        self.__source = source
        self.reset()

    def close(self):
        pass

    def reset(self):
        self.__items = self.__emit_items()

    @property
    def items(self):
        return self.__items

    # Private

    def __emit_items(self):
        items = self.__source
        for item in items:
            if isinstance(item, (tuple, list)):
                yield (None, tuple(item))
            elif isinstance(item, dict):
                keys = []
                values = []
                for key in sorted(item.keys()):
                    keys.append(key)
                    values.append(item[key])
                yield (tuple(keys), tuple(values))
            else:
                raise errors.Error('Native item has to be tuple, list or dict')
