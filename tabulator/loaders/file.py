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

class FileLoader(api.Loader):
    """Loader to load source from filesystem.
    """

    # Public

    def __init__(self, **options):
        self.__options = options

    def load(self, source, encoding, mode):

        # Prepare source
        scheme = 'file://'
        if source.startswith(scheme):
            source = source.replace(scheme, '', 1)

        # Prepare bytes
        bytes = io.open(source, 'rb')

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
