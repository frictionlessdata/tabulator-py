# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

from .iterator import Iterator
from . import errors


# Module API

class Table(object):
    """Table representation.

    NOTE: constructor is not a part of public API

    Args:
        loader (loaders.API): table loader
        parser (parsers.API): table parser

    """

    # Public

    def __init__(self, loader, parser):
        self.__loader = loader
        self.__parser = parser
        self.__processors = []
        self.__iterator = None
        self.__headers = None
        self.__keyed = False

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
        return self

    def __next__(self):

        # Check not closed
        self.__require_not_closed()

        # Get the next row
        self.__iterator.__next__()
        if self.__keyed:
            if self.__iterator.headers is None:
                raise ValueError('Headers are required for keyed output')
            row = dict(zip(self.__iterator.headers, self.__iterator.values))
        else:
            row = tuple(self.__iterator.values)

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

        # Open parser, create iterator
        if self.closed:
            self.__parser.open(self.__loader)
            self.__iterator = Iterator(self.__parser.items, self.__processors)

        return self

    def close(self):
        """Close table by closing underlaying stream.
        """

        # Close parser, remove iterator
        if not self.closed:
            self.__parser.close()
            self.__iterator = None

    @property
    def closed(self):
        """Return true if table is closed.
        """
        return self.__parser.closed or self.__iterator is None

    def reset(self):
        """Reset table pointer to the first row.
        """

        # Check not closed
        self.__require_not_closed()

        # Reset parser, recreate iterator
        self.__parser.reset()
        self.__iterator = Iterator(self.__parser.items, self.__processors)

    @property
    def headers(self):
        """Return table headers.
        """

        # Retrieve headers
        if self.__iterator.count == 0:
            self.__iterator.__next__(lookahead=True)

        return self.__iterator.headers

    def iter(self, keyed=False):
        # Temporal sulution untile main iter
        # logic will be moved here
        self.__keyed = keyed
        return self

    def readrow(self):
        """Return the next row from the table.
        """
        return next(self)

    def read(self, limit=None):
        """Return full table with row limit.

        Parameters
        ----------
        limit: int
            Rows limit to return.

        """

        # Collect rows
        rows = []
        for count, row in enumerate(self, start=1):
            if limit is not None:
                if count > limit:
                    break
            rows.append(row)

        return rows

    # Private

    def __require_not_closed(self):

        # Raise error
        if self.closed:
            message = (
               'Table have to be opened by `table.open()` before '
               'iteration interface will be available.')
            raise errors.Error(message)

    # Python2 support
    next = __next__
