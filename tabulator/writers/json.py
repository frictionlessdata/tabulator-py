# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import six
import json
from ..writer import Writer
from .. import helpers


# Module API

class JSONWriter(Writer):
    """JSON writer.
    """

    # Public

    options = [
        'keyed',
    ]

    def __init__(self, keyed=False):
        self.__keyed = keyed

    def write(self, source, target, headers, encoding=None):
        helpers.ensure_dir(target)
        data = []
        if not self.__keyed:
            data.append(headers)
        for row in source:
            if self.__keyed:
                row = zip(headers, row)
            data.append(row)
        with open(target, 'w') as file:
            json.dump(data, file, indent=2)
