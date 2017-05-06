# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import shutil
import openpyxl
from tempfile import TemporaryFile
from ..parser import Parser
from .. import helpers


# Module API

class XLSXParser(Parser):
    """Parser to parse Excel modern `xlsx` data format.
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
        self.__bytes = self.__loader.load(
            source, mode='b', encoding=encoding, allow_zip=True)
        # For remote stream we need local copy (will be deleted on close by Python)
        # https://docs.python.org/3.5/library/tempfile.html#tempfile.TemporaryFile
        if hasattr(self.__bytes, 'url'):
            new_bytes = TemporaryFile()
            shutil.copyfileobj(self.__bytes, new_bytes)
            self.__bytes.close()
            self.__bytes = new_bytes
            self.__bytes.seek(0)
        self.__book = openpyxl.load_workbook(self.__bytes, read_only=True, data_only=True)
        self.__sheet = self.__book.worksheets[self.__index]
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
        for row_number, row in enumerate(self.__sheet.iter_rows(), start=1):
            yield (row_number, None, list(cell.value for cell in row))
