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

    options = []

    def load(self, source, encoding, mode):

        # Prepare source
        scheme = 'file://'
        if source.startswith(scheme):
            source = source.replace(scheme, '', 1)

        # Prepare bytes
        try:
            bytes = io.open(source, 'rb')
        except IOError as exception:
            raise exceptions.IOError(str(exception))

        # Prepare encoding
        encoding = helpers.detect_encoding(bytes, encoding)

        # Return or raise
        if mode == 'b':
            return bytes
        else:
            chars = io.TextIOWrapper(bytes, encoding)
            return chars
