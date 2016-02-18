# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

from . import errors


# Module API

class Iterator(object):
    """Iterator representation.
    """

    # Public

    def __init__(self, items, processors):
        self.__items = items
        self.__processors = processors
        self.__index = None
        self.__count = 0
        self.__keys = None
        self.__values = None
        self.__headers = None
        self.__is_stop = False
        self.__is_skip = False
        self.__lookahead = False
        self.__exception = None

    def __iter__(self):
        return self

    def __next__(self, lookahead=False):

        # Return if lookahead is set on prev iteration
        if self.__lookahead and not lookahead:
            self.__lookahead = False
            return self

        # Stop iteration
        if self.__is_stop:
            raise StopIteration()

        # Update index
        if self.__index is None:
            self.__index = 0
        else:
            self.__index += 1

        # Reset variables
        self.__keys = None
        self.__values = None
        self.__is_stop = False
        self.__is_skip = False

        # Get next keys, values from items
        try:
            self.__keys, self.__values = next(self.__items)
        except StopIteration:
            raise
        except Exception as exception:
            self.__exception = exception

        # Process iterator by processors
        for processor in self.__processors:
            if self.__exception is None:
                processor.process(self)
            else:
                processor.handle(self)
            if self.__is_skip:
                break

        # Raise if there is active exception
        if self.__exception is not None:
            raise self.__exception

        # Skip iteration
        if self.__is_skip:
            return self.__next__(lookahead)

        # Update count
        self.__count += 1

        # Set lookahead
        self.__lookahead = lookahead

        return self

    def __repr__(self):

        # Template and format
        template = (
            'Iterator <{self.index}, {self.count}, '
            '{self.headers}, {self.values}>')
        result = template.format(self=self)

        return result

    def skip(self):
        """Skip current iteration.
        """
        self.__is_skip = True

    def stop(self):
        """Stop iteration process.
        """
        self.__is_stop = True

    @property
    def index(self):
        """Item index from underlaying stream.

        Before iteration: None
        On first item: 0
        On second item: 1
        ...

        """
        return self.__index

    @property
    def count(self):
        """Count of non skipped items.

        Before iteration: 0
        After first non skipped item: 1
        After second non skipped item: 2
        ...

        """
        return self.__count

    @property
    def keys(self):
        """Item keys.
        """
        return self.__keys

    @property
    def values(self):
        """Item values.
        """
        return self.__values

    @values.setter
    def values(self, values):
        """Set item values.

        Parameters
        ----------
        values: tuple

        """
        self.__values = values

    @property
    def headers(self):
        """Item headers.
        """
        return self.__headers

    @headers.setter
    def headers(self, headers):
        """Set item headers.

        Parameters
        ----------
        headers: tuple

        """
        if self.__count != 0:
            message = 'Headers could be set only before first item is emited.'
            raise errors.Error(message)
        self.__headers = headers

    @property
    def exception(self):
        """Current exception.
        """
        return self.__exception

    # Python2 support
    next = __next__
