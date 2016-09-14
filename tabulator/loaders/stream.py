# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import io
from .. import exceptions
from .. import helpers
from . import api


# Module API

class StreamLoader(api.Loader):
    """Loader to load source from file-like byte stream.
    """

    # Public

    def __init__(self, **options):
        self.__options = options

    def load(self, source, encoding, mode):

        # Raise if in text mode
        if hasattr(source, 'encoding'):
            message = 'Only byte streams are supported.'
            raise exceptions.LoadingError(message)

        # Prepare bytes
        bytes = source

        # Prepare encoding
        encoding = helpers.detect_encoding(bytes, encoding)

        # Return or raise
        if mode == 'b':
            return bytes
        elif mode == 't':
            chars = io.TextIOWrapper(bytes, encoding, **self.__options)
            return chars
        else:
            message = 'Mode %s is not supported' % mode
            raise exceptions.LoadingError(message)
