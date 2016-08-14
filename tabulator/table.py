# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import six


# Module API

class Table(object):
    """Table representation.

    NOTE: constructor is not a part of public API

    Args:
        source (str): table source
        headers (list/str): headers list/pointer
        encoding (str): encoding of source
        loader (loaders.API): table loader
        parser (parsers.API): table parser

    """

    # Public

    def __init__(self, source, headers, encoding, loader, parser):
        self.__source = source
        self.__headers = headers
        self.__encoding = encoding
        self.__loader = loader
        self.__parser = parser
        self.__extracted_headers = None

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
        """Return rows iterator.
        """
        return self.iter()

    @property
    def closed(self):
        """Return true if table is closed.
        """
        return self.__parser.closed

    def open(self):
        """Open table to iterate over it.
        """
        # Here could be moved detect_encoding and detect_html
        # We could cache rows for detections and full headers support
        self.__parser.open(self.__source, self.__encoding, self.__loader)
        self.__extract_headers()
        return self

    def close(self):
        """Close table by closing underlaying stream.
        """
        self.__parser.close()

    def reset(self):
        """Reset table pointer to the first row.
        """
        self.__parser.reset()
        self.__extract_headers()

    @property
    def headers(self):
        """list: table headers

        If source is keyed and headers are not provided by user
        this property will be None because for keyed sources
        headers could differ across rows.

        """
        return self.__extracted_headers

    def iter(self, keyed=False, extended=False):
        """Return rows iterator.

        Args:
            keyed (bool): yield keyed rows
            extended (bool): yield extended rows

        Yields:
            mixed[]/mixed{}: row/keyed row/extended row

        """
        for number, headers, row in self.__parser.extended_rows:
            if headers is None:
                headers = self.headers
            if extended:
                yield (number, headers, row)
            elif keyed:
                yield dict(zip(headers, row))
            else:
                yield row

    def read(self, keyed=False, extended=False, limit=None):
        """Return table rows with count limit.

        Args:
            keyed (bool): return keyed rows
            extended (bool): return extended rows
            limit (int): rows count limit

        Returns:
            list: rows/keyed rows/extended rows
        """
        result = []
        rows = self.iter(keyed=keyed, extended=extended)
        for count, row in enumerate(rows, start=1):
            if count == limit:
                break
            result.append(row)
        return result

    # Private

    def __extract_headers(self):
        # There could be a cleaner way to work with headers
        # But extraction def should be on open and reset
        self.__extracted_headers = self.__headers
        # We've got headers pointer like `row1` (validate)
        if isinstance(self.__extracted_headers, six.string_types):
            pointer = int(self.__extracted_headers.replace('row', ''))
            for number, headers, row in self.__parser.extended_rows:
                if number == pointer:
                    self.__extracted_headers = row
                    break
