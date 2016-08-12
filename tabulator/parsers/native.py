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
        self.__extended_rows = None
        self.__options = options
        self.__source = None

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
        self.__extended_rows = self.__iter_extended_rows()

    @property
    def extended_rows(self):
        return self.__extended_rows

    # Private

    def __iter_extended_rows(self):
        items = self.__source
        for index, item in enumerate(items):
            if isinstance(item, (tuple, list)):
                yield (index, None, tuple(item))
            elif isinstance(item, dict):
                keys = []
                values = []
                for key in sorted(item.keys()):
                    keys.append(key)
                    values.append(item[key])
                yield (index, tuple(keys), tuple(values))
            else:
                raise errors.Error('Native item has to be tuple, list or dict')
