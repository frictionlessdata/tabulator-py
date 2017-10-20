# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import io
import six
from six.moves.urllib.error import URLError
from six.moves.urllib.request import Request, urlopen
from ..loader import Loader
from .. import exceptions
from .. import helpers
from .. import config


# Module API

class RemoteLoader(Loader):
    """Loader to load source from the web.
    """

    # Public

    options = [
        'http_stream',
    ]

    def __init__(self, bytes_sample_size=config.DEFAULT_BYTES_SAMPLE_SIZE,
                 http_stream=True):

        # No stream support
        if six.PY2:
            http_stream = False

        # Set attributes
        self.__bytes_sample_size = bytes_sample_size
        self.__http_stream = http_stream

    def load(self, source, mode='t', encoding=None):

        # Prepare source
        source = helpers.requote_uri(source)

        # Prepare bytes
        try:
            if self.__http_stream:
                bytes = _WebStream(source)
                response = bytes.response
            else:
                response = urlopen(source)
                bytes = io.BufferedRandom(io.BytesIO())
                bytes.write(response.read())
                bytes.seek(0)
        except URLError as exception:
            raise exceptions.HTTPError(str(exception))

        # Return bytes
        if mode == 'b':
            return bytes

        # Detect encoding
        if self.__bytes_sample_size:
            sample = bytes.read(self.__bytes_sample_size)
            bytes.seek(0)
            encoding = helpers.detect_encoding(sample, encoding)

        # Prepare chars
        chars = io.TextIOWrapper(bytes, encoding)

        return chars


# Internal

class _WebStream(object):

    # Public

    def __init__(self, source):
        self.__source = source
        self.__request = Request(self.__source, headers=config.HTTP_HEADERS)
        self.__response = urlopen(self.__request)

    def __getattr__(self, name):
        return getattr(self.__response, name)

    @property
    def response(self):
        return self.__response

    def seekable(self):
        return True

    def seek(self, offset, whence=0):
        assert offset == 0
        assert whence == 0
        self.__response = urlopen(self.__request)
