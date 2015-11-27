# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import io
import six
from six.moves.urllib.request import urlopen
from .. import errors
from .api import API


class Web(API):
    """Loader to load source from the web.
    """

    # Public

    def __init__(self, source, encoding=None, stream=False):
        self.__source = source
        self.__encoding = encoding
        self.__stream = stream

    def load(self, mode):

        # Prepare response
        response = urlopen(self.__source)

        # Prepare bytes
        if self.__stream:
            bytes = response
        else:
            bytes = io.BufferedRandom(io.BytesIO())
            bytes.write(response.read())
            bytes.seek(0)

        # Prepare encoding
        if six.PY2:
            encoding = response.headers.getparam('charset')
        else:
            encoding = response.headers.get_content_charset()
        if self.__encoding is not None:
            encoding = self.__encoding

        # Return or raise
        if mode == 'b':
            return (bytes, encoding)
        elif mode == 't':
            chars = io.TextIOWrapper(bytes, encoding)
            return chars
        else:
            message = 'Mode %s is not supported' % mode
            raise errors.Error(message)
