# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import six
from ..parser import Parser
from .. import exceptions


# Module API

class InlineParser(Parser):
    """Parser to provide support for python inline lists.
    """

    # Public

    options = []

    def __init__(self, loader):
        self.__loader = loader
        self.__force_parse = None
        self.__extended_rows = None
        self.__source = None

    @property
    def closed(self):
        return True

    def open(self, source, encoding=None, force_parse=False):
        if hasattr(source, '__next__' if six.PY3 else 'next'):
            message = 'Only callable returning an iterator is supported'
            raise exceptions.SourceError(message)
        self.close()
        self.__force_parse = force_parse
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
        for row_number, item in enumerate(items, start=1):
            if isinstance(item, (tuple, list)):
                yield (row_number, None, list(item))
            elif isinstance(item, dict):
                keys = []
                values = []
                for key in sorted(item.keys()):
                    keys.append(key)
                    values.append(item[key])
                yield (row_number, list(keys), list(values))
            else:
                if not self.__force_parse:
                    message = 'Inline data item has to be tuple, list or dict'
                    raise exceptions.SourceError(message)
                yield (row_number, None, [])
