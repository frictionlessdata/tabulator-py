# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import ijson
from .. import exceptions
from .. import helpers
from . import api


# Module API

class JSONParser(api.Parser):
    """Parser to parse JSON data format.
    """

    # Public

    def __init__(self, path=None):
        self.__extended_rows = None
        self.__path = path
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
        prefix = 'item'
        if self.__path is not None:
            prefix = '%s.item' % self.__path
        items = ijson.items(self.__chars, prefix)
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
                message = 'JSON item has to be list or dict'
                raise exceptions.ParsingError(message)
