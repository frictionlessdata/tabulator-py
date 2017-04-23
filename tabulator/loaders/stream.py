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

class StreamLoader(Loader):
    """Loader to load source from file-like byte stream.
    """

    # Public

    options = []

    def load(self, source, mode='t', encoding=None, allow_zip=False):

        # Raise if in text mode
        if hasattr(source, 'encoding'):
            message = 'Only byte streams are supported.'
            raise exceptions.SourceError(message)

        # Prepare bytes
        bytes = source
        sample = bytes.read(config.BYTES_SAMPLE_SIZE)
        bytes.seek(0)
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
