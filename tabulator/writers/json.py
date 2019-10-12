# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import six
import json

# from tabulator import Stream

from ..writer import Writer
from .. import helpers


# Module API

class JSONWriter(Writer):
    """JSON writer.
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

    def write(self, source, target, headers=None, encoding=None):
        helpers.ensure_dir(target)
        jsonfile = open(target, 'w')
        out = []
        dict1 = {}
        for row in source:
            for i in range(len(row)):
                dict1.update({headers[i]: row[i]})
            out.append(dict1.copy())
        json.dump(out, jsonfile, ensure_ascii=False, encoding='utf8')
        jsonfile.write('\n')
