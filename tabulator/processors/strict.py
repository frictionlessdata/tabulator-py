# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

from .. import errors
from . import api


# Module API

class StrictProcessor(api.Processor):
    """Processor to ensure the same headers and dimension of the rows.
    """

    # Public

    def __init__(self, skip=False):
        self.__skip = skip
        self.__headers = None
        self.__dimension = None

    def process(self, iterator):

        # Error flag
        error = False

        # Check headers
        if self.__headers is None:
            self.__headers = iterator.headers
        else:
            if self.__headers != iterator.headers:
                error = 'headers are not consistent'

        # Check dimension
        if self.__dimension is None:
            self.__dimension = len(iterator.values)
        else:
            if self.__dimension != len(iterator.values):
                error = 'dimensions are not consistent'

        # Check headers/dimension
        if self.__headers is not None:
            if self.__dimension != len(self.__headers):
                error = 'headers/values have different dimensions'

        # Skip or raise exception
        if error:
            if self.__skip:
                return iterator.skip()
            raise errors.Error('Strict error: %s' % error)

    def handle(self, iterator):
        pass  # pragma: no cover
