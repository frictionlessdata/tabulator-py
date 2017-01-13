# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import io
import os


# General

from .stream import Stream
from . import exceptions

# Deprecated

from .topen import topen
from .stream import Stream as Table

# Version

__version__ = io.open(
    os.path.join(os.path.dirname(__file__), 'VERSION'),
    encoding='utf-8').read().strip()
