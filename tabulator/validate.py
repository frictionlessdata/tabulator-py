# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

from . import config
from . import helpers


# Module API

def validate(source, scheme=None, format=None):
    """https://github.com/frictionlessdata/tabulator-py#validate
    """
    if scheme is None:
        scheme = helpers.detect_scheme(source)
    if scheme is not None:
        if scheme not in config.LOADERS:
            return False
    if format is None:
        format = helpers.detect_format(source)
    if format not in config.PARSERS:
        return False
    return True
