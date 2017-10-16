# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import six
import xlrd
from ..parser import Parser
from .. import exceptions
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

    def __init__(self, loader, force_parse=False, sheet=1, fill_merged_cells=False):
        self.__loader = loader
        self.__sheet_pointer = sheet
        self.__fill_merged_cells = fill_merged_cells
        self.__force_parse = force_parse
        self.__extended_rows = None
        self.__encoding = None
        self.__bytes = None

    @property
    def closed(self):
        return self.__bytes is None or self.__bytes.closed

    def open(self, source, encoding=None):
        self.close()
        self.__encoding = encoding
        self.__bytes = self.__loader.load(source, mode='b', encoding=encoding)

        # Get book
        self.__book = xlrd.open_workbook(
            file_contents=self.__bytes.read(),
            encoding_override=encoding,
            formatting_info=True)

        # Get sheet
        try:
            if isinstance(self.__sheet_pointer, six.string_types):
                self.__sheet = self.__book.sheet_by_name(self.__sheet_pointer)
            else:
                self.__sheet = self.__book.sheet_by_index(self.__sheet_pointer - 1)
        except (xlrd.XLRDError, IndexError):
            message = 'Excel document "%s" doesn\'t have a sheet "%s"'
            raise exceptions.SourceError(message % (source, self.__sheet_pointer))

        # Reset parser
        self.reset()

    def close(self):
        if not self.closed:
            self.__bytes.close()

    def reset(self):
        helpers.reset_stream(self.__bytes)
        self.__extended_rows = self.__iter_extended_rows()

    @property
    def encoding(self):
        return self.__encoding

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
