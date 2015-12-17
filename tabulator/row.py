# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

from . import errors


class Row(tuple):

    # Public

    def __new__(cls, headers, values):
        return super(Row, cls).__new__(cls, tuple(values))

    def __init__(self, headers, values):
        self.__headers = headers
        self.__mapping = None
        if headers is not None:
            self.__mapping = dict(zip(headers, values))

    def get(self, header):
        if self.__mapping is None:
            raise errors.Error('No headers are available.')
        return self.__mapping[header]
