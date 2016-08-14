# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

from . import helpers


# Module API

@helpers.bindify
def skip_comments(extended_rows, mark='#'):
    for number, headers, row in extended_rows:
        if row and hasattr(row[0], 'startswith') and row[0].startswith(mark):
            continue
        yield (number, headers, row)


@helpers.bindify
def skip_blank(extended_rows):
    for number, headers, row in extended_rows:
        if not row:
            continue
        yield (number, headers, row)


@helpers.bindify
def convert(extended_rows, converter=None):
    if converter is None:
        converter = helpers.convert_row
    for number, headers, row in extended_rows:
        yield (number, headers, converter(row))
