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
        'fill_merged_cells',
    ]

    def __init__(self, loader, sheet=1, fill_merged_cells=False):
        self.__loader = loader
        self.__index = sheet - 1
        self.__fill_merged_cells = fill_merged_cells
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
                encoding_override=encoding,
                formatting_info=True)
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
        for x in range(0, self.__sheet.nrows):
            row_number = x + 1
            row = []
            for y, value in enumerate(self.__sheet.row_values(x)):
                if self.__fill_merged_cells:
                    for xlo, xhi, ylo, yhi in self.__sheet.merged_cells:
                        if x in range(xlo, xhi) and y in range(ylo, yhi):
                            value = self.__sheet.cell_value(xlo, ylo)
                row.append(value)
            yield (row_number, None, row)
