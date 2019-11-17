# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import six
import openpyxl
from ..writer import Writer
from .. import helpers


# Module API

class XLSXWriter(Writer):
    """XLXX writer.
    """

    # Public

    options = [
        'sheet',
    ]

    def __init__(self, **options):

        # Make bytes
        if six.PY2:
            for key, value in options.items():
                if isinstance(value, six.string_types):
                    options[key] = str(value)

        # Set attributes
        self.__options = options

    def write(self, source, target, headers, encoding=None):
        helpers.ensure_dir(target)
        wb = openpyxl.Workbook(write_only=True)
        ws = wb.create_sheet(title=self.__options.get('sheet'))
        ws.append(headers)
        for row in source:
            ws.append(row)
        wb.save(target)
