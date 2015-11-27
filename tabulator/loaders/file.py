# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import io
import sys
from .. import errors
from .api import API


class File(API):
    """Loader to load source from filesystem.
    """

    # Public

    def __init__(self, source, encoding=None):
        self.__source = source
        self.__encoding = encoding

    def load(self, mode):

        # Prepare source
        schema = 'file://'
        source = self.__source
        if source.startswith(schema):
            source = source.replace(schema, '', 1)

        # Prepare bytes
        bytes = io.open(source, 'rb')

        # Prepare encoding
        encoding = sys.getdefaultencoding()
        if self.__encoding is not None:
            encoding = self.__encoding

        # Return or raise
        if mode == 'b':
            return (bytes, encoding)
        elif mode == 't':
            chars = io.TextIOWrapper(bytes, self.__encoding)
            return chars
        else:
            message = 'Mode %s is not supported' % mode
            raise errors.Error(message)
