# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

from . import errors


# Module API

class Row(tuple):
    """Row representation.
    """

    # Public

    def __new__(cls, headers, values):
        return super(Row, cls).__new__(cls, tuple(values))

    def __init__(self, headers, values):

        # Set attributes
        self.__headers = headers
        self.__values = values

        # Create mapping
        self.__mapping = None
        if headers is not None:
            self.__mapping = dict(zip(headers, values))

    @property
    def headers(self):
        """Return headers.
        """
        return self.__headers

    @property
    def values(self):
        """Return values.
        """
        return self.__values

    def get(self, header):
        """Get value by header.

        Parameters
        ----------
        header: str
            Header name.

        """

        # If no headers
        if self.__mapping is None:
            raise errors.Error('No headers are available.')

        return self.__mapping[header]
