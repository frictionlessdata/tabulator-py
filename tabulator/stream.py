# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import six
from . import helpers
from . import exceptions


# Module API

class Stream(object):
    """Tabular stream.

    Args:
        source (str): stream source
        headers (list/str):
            headers list or pointer:
                - list of headers for setting by user
                - row pointer like `row3` to extract headers.
                  For plain source headers row and all rows
                  before will be removed. For keyed source no rows
                  will be removed.
        scheme (str):
            scheme of source:
                - file (default)
                - stream
                - text
                - http
                - https
                - ftp
                - ftps
                - native
        format (str):
            format of source:
                - None (detect)
                - csv
                - tsv
                - json
                - xls
                - xlsx
                - native
        encoding (str):
            encoding of source:
                - None (detect)
                - utf-8
                - <encodings>
        post_parse (generator[]): post parse processors (hooks). Signature
            to follow is "processor(extended_rows)" which should yield
            one extended row (number, headers, row) per yield instruction.
        sample_size (int): rows count for table.sample. Set to "0" to prevent
            any parsing activities before actual table.iter call. In this case
            headers will not be extracted from the source.
        loader_options (dict):
            loader options:
                - `constructor`: constructor returning `loaders.API` instance
                - `encoding`: encoding of source
                - <backend options>
        parser_options (dict):
            parser options:
                - `constructor`: constructor returning `parsers.API` instance
                - <backend options>

    """

    # Public

    def __init__(self,
                 source,
                 headers=None,
                 scheme=None,
                 format=None,
                 encoding=None,
                 post_parse=None,
                 sample_size=None,
                 loader_options=None,
                 parser_options=None,):

        # Initiate if None
        if loader_options is None:
            loader_options = {}
        if parser_options is None:
            parser_options = {}
        if post_parse is None:
            post_parse = []
        if sample_size is None:
            sample_size = helpers.DEFAULT_SAMPLE_SIZE

        # Get loader
        if scheme is None:
            scheme = helpers.detect_scheme(source) or helpers.DEFAULT_SCHEME
        if scheme not in helpers.LOADERS:
            message = 'Scheme "%s" is not supported' % scheme
            raise exceptions.LoadingError(message)
        loader = helpers.LOADERS[scheme](**loader_options)

        # Get parser
        if format is None:
            format = helpers.detect_format(source)
        if format not in helpers.PARSERS:
            message = 'Format "%s" is not supported' % format
            raise exceptions.ParsingError(message)
        parser = helpers.PARSERS[format](**parser_options)

        # Set attributes
        self.__source = source
        self.__headers = headers
        self.__encoding = encoding
        self.__post_parse = post_parse
        self.__sample_size = sample_size
        self.__loader = loader
        self.__parser = parser

        # Internal state
        self.__headers_row = None
        self.__headers_list = None
        self.__sample_extended_rows = []
        if isinstance(headers, (tuple, list)):
            self.__headers_list = list(headers)
        elif isinstance(headers, int):
            self.__headers_row = headers
            if headers > sample_size:
                msg = 'Headers row (%s) can\'t be more than sample_size (%s)'
                msg = msg % (self.__headers_row, sample_size)
                raise exceptions.TabulatorException(msg)

    def __enter__(self):
        """Enter context manager by opening table.
        """
        if self.closed:
            self.open()
        return self

    def __exit__(self, type, value, traceback):
        """Exit context manager by closing table.
        """
        if not self.closed:
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
        self.__parser.open(self.__source, self.__encoding, self.__loader)
        self.__prepare_table()
        return self

    def close(self):
        """Close table by closing underlaying stream.
        """
        self.__parser.close()

    def reset(self):
        """Reset table pointer to the first row.
        """
        self.__parser.reset()
        self.__prepare_table()

    @property
    def headers(self):
        """None/list: table headers
        """
        return self.__headers_list

    @property
    def sample(self):
        """list[]: sample of rows
        """
        sample = []
        for number, headers, row in self.__sample_extended_rows:
            sample.append(row)
        return sample

    def iter(self, keyed=False, extended=False):
        """Return rows iterator.

        Args:
            keyed (bool): yield keyed rows
            extended (bool): yield extended rows

        Yields:
            mixed[]/mixed{}: row/keyed row/extended row

        """
        extended_rows = self.__iter_exteneded_rows()
        for processor in self.__post_parse:
            extended_rows = processor(extended_rows)
        for number, headers, row in extended_rows:
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
            result.append(row)
            if count == limit:
                break
        return result

    def save(self, path, format=None,  encoding=None, **writer_options):
        """Save stream to filesystem.
        """
        if format is None:
            format = helpers.detect_format(path)
        if format not in helpers.WRITERS:
            message = 'Format "%s" is not supported' % format
            raise exceptions.WritingError(message)
        if encoding is None:
            encoding = helpers.DEFAULT_ENCODING
        writer = helpers.WRITERS[format]()
        writer.write(path, encoding, self, self.headers, **writer_options)

    # Private

    def __prepare_table(self):

        # Extract sample
        self.__sample_extended_rows = []
        keyed_source = False
        if self.__sample_size:
            for _ in range(self.__sample_size):
                try:
                    (number, headers, row) = next(self.__parser.extended_rows)
                    if headers is not None:
                        keyed_source = True
                    self.__sample_extended_rows.append((number, headers, row))
                except StopIteration:
                    break

        # Detect html content
        if not keyed_source:
            text = ''
            for number, headers, row in self.__sample_extended_rows:
                for value in row:
                    if isinstance(value, six.string_types):
                        text += value
            html_source = helpers.detect_html(text)
            if html_source:
                msg = 'Source has been detected as HTML (not supported)'
                raise exceptions.TabulatorException(msg)

        # Extract headers
        if self.__headers_row:
            for number, headers, row in self.__sample_extended_rows:
                if number == self.__headers_row:
                    if keyed_source:
                        self.__headers_list = headers
                    else:
                        self.__headers_list = row

        # Remove headers from sample
        if not keyed_source:
            self.__sample_extended_rows = self.__sample_extended_rows[
                self.__headers_row:]

    def __iter_exteneded_rows(self):

        # Iter from sample adding headers
        while self.__sample_extended_rows:
            number, headers, row = self.__sample_extended_rows.pop(0)
            if headers is None:
                headers = self.__headers_list
            yield (number, headers, row)

        # Iter following rows from parser adding headers
        for number, headers, row in self.__parser.extended_rows:
            if headers is None:
                headers = self.__headers_list
            yield (number, headers, row)
