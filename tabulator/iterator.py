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
        self.__count = None
        self.__keys = None
        self.__values = None
        self.__headers = None
        self.__is_stop = False
        self.__is_skip = False
        self.__exception = None

    def __iter__(self):
        return self

    def __next__(self): #noqa

        # Stop iteration
        if self.__is_stop:
            raise StopIteration()

        # Update index
        if self.__index is None:
            self.__index = 0
        else:
            self.__index += 1

        # Update count
        if self.__count is None:
            self.__count = 1
        else:
            self.__count += 1

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
            self.__count -= 1
            return self.__next__()

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
        """Item index from underlaying stream (starts from 0).
        """
        return self.__index

    @property
    def count(self):
        """Count of non skipped items (starts from 1).
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
        if self.__headers is not None:
            raise errors.Error('Headers are immutable.')
        self.__headers = headers

    @property
    def exception(self):
        """Current exception.
        """
        return self.__exception

    # Python2 support
    next = __next__
