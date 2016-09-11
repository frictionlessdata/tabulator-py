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

    def write(self, path, encoding, rows, headers, **options):
        helpers.ensure_dir(path)
        with io.open(path, 'wb') as file:
            writer = unicodecsv.writer(file, encoding=encoding, **options)
            writer.writerow(headers)
            for row in rows:
                writer.writerow(row)
