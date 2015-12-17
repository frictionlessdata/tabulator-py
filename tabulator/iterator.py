# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals


class Iterator(object):
    """Iterator representation.
    """

    # Public

    def __init__(self, items, processors):
        self.__items = items
        self.__processors = processors
        self.__index = 0
        self.__count = 0
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

        # Update indexes, reset vars
        self.__index += 1
        self.__count += 1
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

        # Update headers if keys
        if self.__keys is not None:
            self.__headers = self.__keys

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
        template = (
            'Iterator <{self.index}, {self.count}, '
            '{self.headers}, {self.values}>')
        return template.format(self=self)

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
        """
        return self.__index

    @property
    def count(self):
        """Count of non skipped items.
        """
        return self.__count

    @property
    def headers(self):
        """Row headers.
        """
        return self.__headers

    @headers.setter
    def headers(self, headers):
        """Set row headers.

        Parameters
        ----------
        headers: tuple

        """
        self.__headers = headers

    @property
    def values(self):
        """Row values.
        """
        return self.__values

    @values.setter
    def values(self, values):
        """Set row values.

        Parameters
        ----------
        values: tuple

        """
        self.__values = values

    @property
    def exception(self):
        """Current exception.
        """
        return self.__exception

    # Python2 support
    next = __next__
