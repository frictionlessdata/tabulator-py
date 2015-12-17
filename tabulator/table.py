# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

from .row import Row
from .iterator import Iterator
from . import errors


class Table(object):
    """Table representation.

    Parameters
    ----------
    loader: loaders.API
        Table loader.
    parser: parsers.API
        Table parser.
    iterator_class: object
        Custom iterator class.

    """

    # Public

    def __init__(self, loader, parser, iterator_class=None):
        if iterator_class is None:
            iterator_class = Iterator
        self.__iterator_class = iterator_class
        self.__loader = loader
        self.__parser = parser
        self.__processors = []
        self.__iterator = None
        self.__headers = None

    def __enter__(self):
        """Enter context manager by opening table.
        """
        self.open()
        return self

    def __exit__(self, type, value, traceback):
        """Exit context manager by closing table.
        """
        self.close()

    def __iter__(self):
        self.__require_not_closed()
        return self

    def __next__(self):
        self.__require_not_closed()
        next(self.__iterator)
        row = Row(self.__iterator.headers, self.__iterator.values)
        return row

    def add_processor(self, processor):
        """Add processor to pipeline.

        Parameters
        ----------
        processor: `processors.API`
            Processor to add to pipeline.

        """
        self.__processors.append(processor)

    def open(self):
        """Open table to iterate over it.
        """
        if self.closed:
            self.__parser.open(self.__loader)
            self.__iterator = self.__iterator_class(
                    self.__parser.items, self.__processors)
        return self

    def close(self):
        """Close table by closing underlaying stream.
        """
        if not self.closed:
            self.__parser.close()
            self.__iterator = None

    @property
    def closed(self):
        """Return true if table is closed.
        """
        return self.__parser.closed or self.__iterator is None

    @property
    def headers(self):
        """Return table headers.
        """
        self.__require_not_closed()
        if self.__headers is None:
            if self.__iterator.index == 0:
                for iterator in self.__iterator:
                    if iterator.headers is not None:
                        self.__headers = iterator.headers
                        break
                self.reset()
        return self.__headers

    def readrow(self):
        """Return the next row from the table.
        """
        self.__require_not_closed()
        return next(self)

    def read(self, limit=None):
        """Return full table with row limit.

        Parameters
        ----------
        limit: int
            Rows limit to return.

        """
        self.__require_not_closed()
        rows = []
        for num, row in enumerate(self, start=1):
            if limit is not None:
                if num > limit:
                    break
            rows.append(row)
        return rows

    def reset(self):
        """Reset table pointer to the first row.
        """
        self.__require_not_closed()
        self.__parser.reset()
        self.__iterator = self.__iterator_class(
                self.__parser.items, self.__processors)

    # Private

    def __require_not_closed(self):
        if self.closed:
            message = (
               'Table have to be opened by `table.open()` before '
               'iteration interface will be available.')
            raise errors.Error(message)

    # Python2 support
    next = __next__
