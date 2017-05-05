# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import ezodf
from six import BytesIO
from ..parser import Parser
from .. import helpers


# Module API

class ODSParser(Parser):
    """Parser to parse ODF Spreadsheets.

    Args:
        sheet (int or str): sheet number or name
            First sheet's number is 1.

    """

    # Public

    options = [
        'sheet',
    ]

    def __init__(self, loader, sheet=1):
        self.__loader = loader
        self.__index = sheet - 1 if isinstance(sheet, int) else sheet
        self.__force_parse = None
        self.__extended_rows = None
        self.__bytes = None
        self.__book = None
        self.__sheet = None

    @property
    def closed(self):
        return self.__bytes is None or self.__bytes.closed

    def open(self, source, encoding=None, force_parse=False):
        self.close()
        self.__force_parse = force_parse
        self.__bytes = self.__loader.load(
            source, mode='b', encoding=encoding, allow_zip=True)
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
        for row_number, row in enumerate(self.__sheet.rows(), start=1):
            yield row_number, None, [cell.value for cell in row]
