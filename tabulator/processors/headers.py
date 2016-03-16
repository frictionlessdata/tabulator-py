# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

from . import api


# Module API

class HeadersProcessor(api.Processor):
    """Processor to add headers to row.
    """

    # Public

    def __init__(self, skip=0):
        self.__skip = skip

    def process(self, iterator):

        # Skip items
        if iterator.index < self.__skip:
            # Skip iteration
            iterator.skip()

        # Set headers
        if iterator.index == self.__skip:
            if iterator.keys is not None:
                # Set headers
                iterator.headers = iterator.keys
            else:
                # Set headers
                iterator.headers = iterator.values
                # Skip iteration
                iterator.skip()

    def handle(self, iterator):
        pass  # pragma: no cover
