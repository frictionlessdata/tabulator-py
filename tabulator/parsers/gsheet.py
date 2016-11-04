# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import re
from ..stream import Stream
from . import api


# Module API

class GsheetParser(api.Parser):
    """Parser to parse Google Spreadsheets.
    """

    # Public

    options = []

    def __init__(self):
        self.__stream = None

    @property
    def closed(self):
        return self.__stream is None or self.__stream.closed

    def open(self, source, encoding, loader):
        self.close()
        url = 'https://docs.google.com/spreadsheets/d/%s/export?format=csv&id=%s&gid=%s'
        match = re.search(r'.*/d/(?P<key>[^/]+)/.*(?:gid=(?P<gid>\d+))?.*', source)
        key, gid = '', ''
        if match:
            key = match.group('key')
            gid = match.group('gid') or '0'
        url = url % (key, key, gid)
        self.__stream = Stream(url, format='csv', encoding=encoding).open()
        self.__extended_rows = self.__stream.iter(extended=True)

    def close(self):
        if not self.closed:
            self.__stream.close()

    def reset(self):
        self.__stream.reset()
        self.__extended_rows = self.__iter_extended_rows()

    @property
    def extended_rows(self):
        return self.__extended_rows
