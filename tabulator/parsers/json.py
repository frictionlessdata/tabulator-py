# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import ijson
from .. import helpers, errors
from .api import API


class JSON(API):
    """Parser to parse JSON data format.
    """

    # Public

    def __init__(self, path=None):
        self.__path = path
        self.__bytes = None
        self.__items = None

    def open(self, loader):
        self.close()
        self.__loader = loader
        self.__bytes = loader.load(mode='b')
        self.reset()

    def close(self):
        if not self.closed:
            self.__bytes.close()

    @property
    def closed(self):
        return self.__bytes is None or self.__bytes.closed

    @property
    def items(self):
        return self.__items

    def reset(self):
        helpers.reset_stream(self.__bytes)
        self.__items = self.__emit_items()

    # Private

    def __emit_items(self):
        prefix = 'item'
        if self.__path is not None:
            prefix = '%s.item' % self.__path
        items = ijson.items(self.__bytes, prefix)
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
                message = 'JSON item has to be list or dict'
                raise errors.Error(message)
