# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from collections import namedtuple
from .iterator import Iterator


class Table(object):
    """Table representation.

    Args:
        loader (tabulator.loaders.API): table loader
        parser (tabulator.parsers.API): table parser

    """

    # Public

    def __init__(self, loader, parser):
        self.__loader = loader
        self.__parser = parser
        self.__processors = []
        self.__bytes = None
        self.__items = None
        self.__iterator = None

    def __enter__(self):
        """Enter context manager by opening table.
        """
        self.open()
        return self

    def __exit__(self, type, value, traceback):
        """Exit context manager by closing table.
        """
        self.close()

    def add_processor(self, processor):
        """Add processor to pipeline.
        """
        self.__processors.append(processor)

    def open(self):
        """Open table by opening source stream.
        """
        if self.closed:
            self.__bytes = self.__loader.load()
            self.__items = self.__parser.parse(self.__bytes)
            self.__iterator = Iterator(
                    self.__bytes, self.__items, self.__processors)

    def close(self):
        """Close table by closing source stream.
        """
        if not self.closed:
            self.__bytes.close()

    @property
    def closed(self):
        """Return true if table is closed.
        """
        return not self.__bytes or self.__bytes.closed

    def read(self, with_headers=False, limit=None):
        """Return full table.
        """
        rows = []
        rows_iter = self.readrow(with_headers=with_headers)
        for index, row in enumerate(rows_iter):
            if index > limit:
                break
            rows.append(row)
        return rows

    def readrow(self, with_headers=False):
        """Return next row from the source stream.
        """
        self.__require_not_closed()
        for iterator in self.__iterator:
            row = iterator.values
            if with_headers:
                if iterator.headers is None:
                    raise RuntimeError('No headers are available.')
                Row = namedtuple('Row', iterator.headers)
                row = Row(*iterator.values)
            yield row

    @property
    def headers(self):
        """Return table headers.
        """
        self.__require_not_closed()
        if self.__iterator.headers is None:
            if self.__iterator.index == 0:
                for iterator in self.__iterator:
                    if iterator.headers is not None:
                        break
                self.__iterator.reset()
        return self.__iterator.headers

    def reset(self):
        """Reset pointer to the first row.
        """
        self.__require_not_closed()
        self.__iterator.reset()

    # Private

    def __require_not_closed(self):
        if self.closed:
            message = (
               'Table have to be opened by `table.open()` before '
               'iteration interface will be available.')
            raise RuntimeError(message)
