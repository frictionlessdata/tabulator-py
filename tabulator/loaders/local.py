# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import io
from ..loader import Loader
from .. import exceptions
from .. import helpers
from .. import config


# Module API

class LocalLoader(Loader):
    """Loader to load source from filesystem.
    """

    # Public

    options = []

    def load(self, source, mode='t', encoding=None, allow_zip=False):

        # Prepare source
        scheme = 'file://'
        if source.startswith(scheme):
            source = source.replace(scheme, '', 1)

        # Prepare bytes
        try:
            bytes = io.open(source, 'rb')
            sample = bytes.read(config.BYTES_SAMPLE_SIZE)
            bytes.seek(0)
        except IOError as exception:
            raise exceptions.IOError(str(exception))
        if not allow_zip:
            if helpers.detect_zip(sample):
                message = 'Format has been detected as ZIP (not supported)'
                raise exceptions.FormatError(message)

        # Prepare encoding
        encoding = helpers.detect_encoding(sample, encoding)

        # Return or raise
        if mode == 'b':
            return bytes
        else:
            chars = io.TextIOWrapper(bytes, encoding)
            return chars
