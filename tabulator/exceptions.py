# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals


# Module API

class TabulatorException(Exception):
    """Base Tabulator exception.
    """
    pass


class ParsingError(TabulatorException):
    """Base parsing error.
    """
    pass


class LoadingError(TabulatorException):
    """Base loading error.
    """
    pass
