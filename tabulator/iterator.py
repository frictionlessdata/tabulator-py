# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals


class Iterator(object):
    """Iterator representation.
    """

    # Public

    def __init__(self, parser, processors):
        self.__parser = parser
        self.__processors = processors
        self.__input_index = 0
        self.__output_index = 0
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
        self.__input_index += 1
        self.__output_index += 1
        self.__keys = None
        self.__values = None
        self.__is_stop = False
        self.__is_skip = False

        # Get next keys, values from parser
        try:
            self.__keys, self.__values = next(self.__parser.items)
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
            self.__output_index -= 1
            return self.__next__()

        return self

    def __repr__(self):
        template = (
            'Iterator <{self.input_index}, {self.output_index}, '
            '{self.headers}, {self.values}>')
        return template.format(self=self)

    def reset(self):
        self.__parser.reset()
        self.__input_index = 0
        self.__output_index = 0

    def skip(self):
        self.__is_skip = True

    def stop(self):
        self.__is_stop = True

    @property
    def input_index(self):
        return self.__input_index

    @property
    def output_index(self):
        return self.__output_index

    @property
    def headers(self):
        return self.__headers

    @headers.setter
    def headers(self, headers):
        self.__headers = headers

    @property
    def values(self):
        return self.__values

    @values.setter
    def values(self, values):
        self.__values = values

    @property
    def exception(self):
        return self.__exception

    # Python2 support
    next = __next__
