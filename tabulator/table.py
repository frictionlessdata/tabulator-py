# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from collections import namedtuple


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
        self.__stream = None
        self.__rows = None
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

    def add_processor(self, processor):
        """Add processor to pipeline.
        """
        self.__processors.append(processor)

    def open(self):
        """Open table by opening source stream.
        """
        if self.closed:
            self.__stream = self.__loader.load()
            self.__rows = self.__parser.parse(self.__stream)

    def reset(self):
        """Reset pointer to the first row.
        """
        self.__stream.seek(0)

    def close(self):
        """Close table by closing source stream.
        """
        if self.__stream:
            self.__stream.close()

    @property
    def closed(self):
        """Return true if table is closed.
        """
        return not self.__stream or self.__stream.closed

    @property
    def headers(self):
        """Return table headers.
        """
        if self.__headers is None:
            if self.__stream.tell() == 0:
                for _, _, _ in self.__iterate():
                    if self.__headers is not None:
                        break
                self.__stream.seek(0)
        return self.__headers

    def readrow(self, with_headers=False, limit=None):
        """Return next row from the source stream.
        """
        for index, headers, row in self.__iterate():
            if limit is not None:
                if index > limit:
                    raise StopIteration()
            if with_headers:
                if headers is None:
                    raise RuntimeError('No headers are available.')
                Row = namedtuple('Row', headers)
                row = Row(*row)
            yield row

    def read(self, with_headers=False, limit=None):
        """Return full table.
        """
        return list(self.readrow(with_headers=with_headers, limit=limit))

    # Private

    def __iterate(self):
        if self.closed:
            message = (
               'Table have to be opened by `table.open()` before '
               'iteration interface will be available.')
            raise RuntimeError(message)
        index = None
        headers = None
        for row in self.__rows:
            if index is None:
                index = 1
            else:
                index += 1
            for processor in self.__processors:
                if index is None:
                    self.__stream.seek(0)
                    break
                if row is None:
                    break
                index, headers, row = processor.process(index, headers, row)
            if headers is not None:
                self.__headers = headers
            if row is not None:
                yield (index, headers, row)
