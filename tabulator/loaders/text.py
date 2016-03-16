# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import io

from .. import errors
from . import api


# Module API

class TextLoader(api.Loader):
    """Loader to load source from text.
    """

    DEFAULT_ENCODING = 'utf-8'

    # Public

    def __init__(self, source, encoding=None, **options):
        self.__source = source
        self.__encoding = encoding
        self.__options = options

    def load(self, mode):

        # Prepare source
        schema = 'text://'
        source = self.__source
        if source.startswith(schema):
            source = source.replace(schema, '', 1)

        # Prepare encoding
        encoding = self.__encoding
        if encoding is None:
            encoding = self.DEFAULT_ENCODING

        # Prepare bytes
        bytes = io.BufferedRandom(io.BytesIO())
        bytes.write(source.encode(encoding))
        bytes.seek(0)

        # Return or raise
        if mode == 'b':
            return bytes
        elif mode == 't':
            chars = io.TextIOWrapper(bytes, encoding, **self.__options)
            return chars
        else:
            message = 'Mode %s is not supported' % mode
            raise errors.Error(message)

    @property
    def encoding(self):
        return self.__encoding
