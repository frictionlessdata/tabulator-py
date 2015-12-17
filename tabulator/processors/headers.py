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

    def __init__(self, index=1):
        self.__index = index

    def process(self, iterator):

        # Items before headers
        if self.__index > iterator.index:
            if iterator.headers is None:
                # Skip iteration
                iterator.skip()

        # Item has to be headers
        if self.__index == iterator.index:
            if iterator.headers is None:
                # Set headers
                iterator.headers = iterator.values
                # Reset iterator
                if self.__index > 1:
                    iterator.reset()
            # Skip iteration
            iterator.skip()

    def handle(self, iterator):
        pass  # pragma: no cover
