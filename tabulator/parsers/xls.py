# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import xlrd
from ..parser import Parser
from .. import helpers


# Module API

class XLSParser(Parser):
    """Parser to parse Excel data format.
    """

    # Public

    options = [
        'sheet',
    ]

    def __init__(self, loader, sheet=1):
        self.__loader = loader
        self.__index = sheet - 1
        self.__force_parse = None
        self.__extended_rows = None
        self.__bytes = None

    @property
    def closed(self):
        return self.__bytes is None or self.__bytes.closed

    def open(self, source, encoding=None, force_parse=False):
        self.close()
        self.__force_parse = force_parse
        self.__bytes = self.__loader.load(source, mode='b', encoding=encoding)
        self.__book = xlrd.open_workbook(
                file_contents=self.__bytes.read(),
                encoding_override=encoding)
        self.__sheet = self.__book.sheet_by_index(self.__index)
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
        for row_number in range(1, self.__sheet.nrows+1):
            yield (row_number, None, list(self.__sheet.row_values(row_number - 1)))
