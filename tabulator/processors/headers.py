# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

from .api import API


class Headers(API):
    """Processor to add headers to row.
    """

    # Public

    def __init__(self, skip=0):
        self.__skip = skip

    def process(self, iterator):

        # Skip items
        if iterator.index <= self.__skip:
            # Skip iteration
            iterator.skip()

        # Set headers
        if iterator.index == self.__skip:
            iterator.headers = iterator.values

    def handle(self, iterator):
        pass  # pragma: no cover
