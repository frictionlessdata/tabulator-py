# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import io
import unicodecsv
from .. import helpers
from . import api


# Module API

class CSVWriter(api.Writer):
    """CSV writer.
    """

    # Public

    def write(self, target, encoding, extended_rows, **options):
        helpers.ensure_dir(target)
        with io.open(target, 'wb') as file:
            writer = unicodecsv.writer(file, encoding=encoding, **options)
            iterator = enumerate(extended_rows, start=1)
            for count, (_, headers, row) in iterator:
                if count == 1 and headers:
                    writer.writerow(headers)
                writer.writerow(row)
