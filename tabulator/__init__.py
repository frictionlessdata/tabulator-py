# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import io
import json
from .errors import Error
from .iterator import Iterator
from .row import Row
from .table import Table
from .topen import topen


def read(path):
    """Read a text file at the given relative path."""
    basedir = os.path.dirname(__file__)
    return io.open(os.path.join(basedir, path), encoding='utf-8').read()


INFO = json.loads(read('info.json'))

__version__ = INFO['version']
