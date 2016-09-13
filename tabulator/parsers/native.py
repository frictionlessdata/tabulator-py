# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import six
from .. import exceptions
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
        return True

    def open(self, source, encoding, loader):
        if hasattr(source, '__next__' if six.PY3 else 'next'):
            message = 'Only callable returning an iterator is supported'
            raise exceptions.ParsingError(message)
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
        if not hasattr(items, '__iter__'):
            items = items()
        for number, item in enumerate(items, start=1):
            if isinstance(item, (tuple, list)):
                yield (number, None, list(item))
            elif isinstance(item, dict):
                keys = []
                values = []
                for key in sorted(item.keys()):
                    keys.append(key)
                    values.append(item[key])
                yield (number, list(keys), list(values))
            else:
                message = 'Native item has to be tuple, list or dict'
                raise exceptions.ParsingError(message)
