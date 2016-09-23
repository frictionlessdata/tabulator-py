# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import openpyxl
from .. import helpers
from . import api


# Module API

class ExcelxParser(api.Parser):
    """Parser to parse Excel modern `xlsx` data format.
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
        self.__book = openpyxl.load_workbook(self.__bytes, read_only=True)
        self.__sheet = self.__book.worksheets[self.__sheet_index]
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
        for number, row in enumerate(self.__sheet.iter_rows(), start=1):
            yield (number, None, list(cell.value for cell in row))
