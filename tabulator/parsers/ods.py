# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import ezodf
from six import BytesIO

from .. import helpers
from . import api


# Module API

class ODSParser(api.Parser):
    """Parser to parse ODF Spreadsheets.

    Args:
        sheet (int or str): sheet number or name
            First sheet's number is 1.

    """

    # Public

    options = [
        'sheet',
    ]

    def __init__(self, sheet=1):
        self.__index = sheet - 1 if isinstance(sheet, int) else sheet
        self.__loader = None
        self.__bytes = None
        self.__book = None
        self.__sheet = None
        self.__extended_rows = None

    @property
    def closed(self):
        return self.__bytes is None or self.__bytes.closed

    def open(self, source, encoding, loader):
        self.close()
        self.__loader = loader
        self.__bytes = loader.load(source, encoding, mode='b', allow_zip=True)
        self.__book = ezodf.opendoc(BytesIO(self.__bytes.read()))
        self.__sheet = self.__book.sheets[self.__index]
        self.reset()

    def close(self):
        if not self.closed:
            self.__bytes.close()

    def reset(self):
        helpers.reset_stream(self.__bytes)
        self.__extended_rows = self.__iter_extended_rows()

    @property
    def extended_rows(self):
        return self.__extended_rows

    # Private

    def __iter_extended_rows(self):
        for number, row in enumerate(self.__sheet.rows(), start=1):
            yield number, None, [cell.value for cell in row]
