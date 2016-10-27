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


class SourceError(TabulatorException):
    """Stream error.
    """
    pass


class SchemeError(TabulatorException):
    """Scheme error.
    """
    pass


class FormatError(TabulatorException):
    """Format error.
    """
    pass


class EncodingError(TabulatorException):
    """Encoding error.
    """
    pass


class OptionsError(TabulatorException):
    """Options error.
    """
    pass


class IOError(TabulatorException):
    """IO error.
    """
    pass


class HTTPError(TabulatorException):
    """HTTP error.
    """
    pass


class ResetError(TabulatorException):
    """Reset error.
    """
    pass
