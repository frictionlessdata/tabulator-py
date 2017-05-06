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

    # Get scheme and format
    detected_scheme, detected_format = helpers.detect_scheme_and_format(source)
    scheme = scheme or detected_scheme
    format = format or detected_format

    # Validate scheme and format
    if scheme is not None:
        if scheme not in config.LOADERS:
            return False
    if format not in config.PARSERS:
        return False

    return True
