# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import xlrd
from .. import helpers
from . import api


# Module API

class ExcelParser(api.Parser):
    """Parser to parse Excel data format.
    """

    # Public

    def __init__(self, sheet_index=0):
        self.__sheet_index = sheet_index
        self.__bytes = None
        self.__extended_rows = None

    @property
    def closed(self):
        return self.__bytes is None or self.__bytes.closed

    def open(self, source, encoding, loader):
        self.close()
        self.__loader = loader
        self.__bytes = loader.load(source, encoding, mode='b')
        self.__book = xlrd.open_workbook(
                file_contents=self.__bytes.read(),
                encoding_override=encoding)
        self.__sheet = self.__book.sheet_by_index(self.__sheet_index)
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
        for number in range(1, self.__sheet.nrows+1):
            yield (number, None, list(self.__sheet.row_values(number - 1)))
