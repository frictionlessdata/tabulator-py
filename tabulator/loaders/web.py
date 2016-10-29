# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import io
import six
from six.moves.urllib.error import URLError
from six.moves.urllib.request import urlopen
from .. import exceptions
from .. import helpers
from .. import config
from . import api


# Module API

class WebLoader(api.Loader):
    """Loader to load source from the web.
    """

    # Public

    options = []

    def load(self, source, encoding, mode):

        # Requote uri
        source = helpers.requote_uri(source)

        # Prepare bytes
        try:
            if six.PY2:
                response = urlopen(source)
                bytes = io.BufferedRandom(io.BytesIO())
                bytes.write(response.read())
                bytes.seek(0)
            else:
                bytes = _WebStream(source)
                response = bytes.response
            sample = bytes.read(config.BYTES_SAMPLE_SIZE)
            bytes.seek(0)
        except URLError as exception:
            raise exceptions.HTTPError(str(exception))
        if helpers.detect_zip(sample):
            message = 'Format has been detected as ZIP (not supported)'
            raise exceptions.FormatError(message)

        # Prepare encoding
        if encoding is None:
            if six.PY2:
                encoding = response.headers.getparam('charset')
            else:
                encoding = response.headers.get_content_charset()
        encoding = helpers.detect_encoding(sample, encoding)

        # Return or raise
        if mode == 'b':
            return bytes
        else:
            chars = io.TextIOWrapper(bytes, encoding)
            return chars


# Internal

class _WebStream(object):

    # Public

    def __init__(self, source):
        self.__source = source
        self.__response = urlopen(self.__source)

    def __getattr__(self, name):
        return getattr(self.__response, name)

    @property
    def response(self):
        return self.__response

    def seekable(self):
        return True

    def seek(self, offset):
        assert offset == 0
        self.__response = urlopen(self.__source)
