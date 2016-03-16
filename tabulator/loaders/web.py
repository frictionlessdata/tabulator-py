# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import io
import six
from requests.utils import requote_uri
from six.moves.urllib.request import urlopen

from .. import errors, helpers
from . import api


# Module API

class WebLoader(api.Loader):
    """Loader to load source from the web.
    """

    # Public

    def __init__(self, source, encoding=None, **options):
        self.__source = source
        self.__encoding = encoding
        self.__options = options

    def load(self, mode):

        # Requote uri if it contains spaces etc
        source = requote_uri(self.__source)

        # Prepare bytes
        if six.PY2:
            response = urlopen(source)
            bytes = io.BufferedRandom(io.BytesIO())
            bytes.write(response.read())
            bytes.seek(0)
        else:
            bytes = _WebStream(source)
            response = bytes.response

        # Prepare encoding
        encoding = self.__encoding
        if encoding is None:
            if six.PY2:
                encoding = response.headers.getparam('charset')
            else:
                encoding = response.headers.get_content_charset()
        if encoding is None:
            encoding = helpers.detect_encoding(bytes)

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


# Internal

class _WebStream(object):

    # Public

    def __init__(self, source):
        self.__source = source
        self.__response = self.__make_request()

    def __getattr__(self, name):
        return getattr(self.__response, name)

    @property
    def response(self):
        return self.__response

    def seekable(self):
        return True

    def seek(self, offset):
        if offset != 0:
            message = 'Seek support only 0 offset.'
            raise ValueError(message)
        self.__response = self.__make_request()

    # Private

    def __make_request(self):
        return urlopen(self.__source)
