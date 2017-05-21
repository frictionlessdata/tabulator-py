# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals


# Module API

class TabulatorException(Exception):
    """https://github.com/frictionlessdata/tabulator-py#exceptions
    """
    pass


class IOError(TabulatorException):
    """https://github.com/frictionlessdata/tabulator-py#exceptions
    """
    pass


class HTTPError(TabulatorException):
    """https://github.com/frictionlessdata/tabulator-py#exceptions
    """
    pass


class SourceError(TabulatorException):
    """https://github.com/frictionlessdata/tabulator-py#exceptions
    """
    pass


class SchemeError(TabulatorException):
    """https://github.com/frictionlessdata/tabulator-py#exceptions
    """
    pass


class FormatError(TabulatorException):
    """https://github.com/frictionlessdata/tabulator-py#exceptions
    """
    pass


class EncodingError(TabulatorException):
    """https://github.com/frictionlessdata/tabulator-py#exceptions
    """
    pass


class OptionsError(TabulatorException):
    """https://github.com/frictionlessdata/tabulator-py#exceptions
    """
    pass


class ResetError(TabulatorException):
    """https://github.com/frictionlessdata/tabulator-py#exceptions
    """
    pass
