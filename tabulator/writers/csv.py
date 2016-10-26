# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import io
import six
import unicodecsv
from .. import helpers
from . import api


# Module API

class CSVWriter(api.Writer):
    """CSV writer.
    """

    # Public

    options = [
        'delimiter',
    ]

    def __init__(self, **options):

        # Make bytes
        if six.PY2:
            for key, value in options.items():
                if isinstance(value, six.string_types):
                    options[key] = str(value)

        # Set attributes
        self.__options = options

    def write(self, target, encoding, extended_rows):
        helpers.ensure_dir(target)
        with io.open(target, 'wb') as file:
            writer = unicodecsv.writer(
                file, encoding=encoding, **self.__options)
            iterator = enumerate(extended_rows, start=1)
            for count, (_, headers, row) in iterator:
                if count == 1 and headers:
                    writer.writerow(headers)
                writer.writerow(row)
