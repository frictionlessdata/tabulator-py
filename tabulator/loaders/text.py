# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import io
from ..loader import Loader
from .. import config


# Module API

class TextLoader(Loader):
    """Loader to load source from text.
    """

    # Public

    options = []

    def load(self, source, mode='t', encoding=None, allow_zip=False):

        # Prepare source
        scheme = 'text://'
        if source.startswith(scheme):
            source = source.replace(scheme, '', 1)

        # Prepare encoding
        if encoding is None:
            encoding = config.DEFAULT_ENCODING

        # Prepare bytes
        bytes = io.BufferedRandom(io.BytesIO())
        bytes.write(source.encode(encoding))
        bytes.seek(0)

        # Return or raise
        if mode == 'b':
            return bytes
        else:
            chars = io.TextIOWrapper(bytes, encoding)
            return chars
