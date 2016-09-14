# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import six
from itertools import chain
from . import loaders
from . import parsers
from . import writers
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
                - `encoding`: encoding of source
                - <backend options>
        parser_options (dict):
            parser options:
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

        # Defaults
        if loader_options is None:
            loader_options = {}
        if parser_options is None:
            parser_options = {}
        if post_parse is None:
            post_parse = []
        if sample_size is None:
            sample_size = helpers.DEFAULT_SAMPLE_SIZE

        # Headers
        self.__headers = None
        self.__headers_row = 0
        if isinstance(headers, (tuple, list)):
            self.__headers = list(headers)
        elif isinstance(headers, int):
            self.__headers_row = headers
            if headers > sample_size:
                msg = 'Headers row (%s) can\'t be more than sample_size (%s)'
                msg = msg % (self.__headers_row, sample_size)
                raise exceptions.TabulatorException(msg)

        # Loader
        if scheme is None:
            scheme = helpers.detect_scheme(source) or helpers.DEFAULT_SCHEME
        if scheme not in _LOADERS:
            message = 'Scheme "%s" is not supported' % scheme
            raise exceptions.LoadingError(message)
        self.__loader = _LOADERS[scheme](**loader_options)

        # Parser
        if format is None:
            format = helpers.detect_format(source)
        if format not in _PARSERS:
            message = 'Format "%s" is not supported' % format
            raise exceptions.ParsingError(message)
        self.__parser = _PARSERS[format](**parser_options)

        # Attributes
        self.__source = source
        self.__encoding = encoding
        self.__post_parse = post_parse
        self.__sample_size = sample_size
        self.__sample_extended_rows = []
        self.__number = 0

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
        self.__extract_sample()
        self.__extract_headers()
        self.__detect_html()
        return self

    def close(self):
        """Close table by closing underlaying stream.
        """
        self.__parser.close()

    def reset(self):
        """Reset table pointer to the first row.
        """
        if self.__number > self.__sample_size:
            self.__parser.reset()
            self.__extract_sample()
            self.__extract_headers()
        self.__number = 0

    @property
    def headers(self):
        """None/list: table headers
        """
        return self.__headers

    @property
    def sample(self):
        """list[]: sample of rows
        """
        sample = []
        iterator = iter(self.__sample_extended_rows)
        iterator = self.__apply_processors(iterator)
        for number, headers, row in iterator:
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
        iterator = chain(
            self.__sample_extended_rows,
            self.__parser.extended_rows)
        iterator = self.__apply_processors(iterator)
        for number, headers, row in iterator:
            if number > self.__number:
                self.__number = number
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

    def save(self, target, format=None,  encoding=None, **writer_options):
        """Save stream to filesystem.
        """
        if encoding is None:
            encoding = helpers.DEFAULT_ENCODING
        if format is None:
            format = helpers.detect_format(target)
        if format not in _WRITERS:
            message = 'Format "%s" is not supported' % format
            raise exceptions.WritingError(message)
        extended_rows = self.iter(extended=True)
        writer = _WRITERS[format]()
        writer.write(target, encoding, extended_rows, **writer_options)

    # Private

    def __extract_sample(self):

        # Extract sample
        self.__sample_extended_rows = []
        if self.__sample_size:
            for _ in range(self.__sample_size):
                try:
                    number, headers, row = next(self.__parser.extended_rows)
                    self.__sample_extended_rows.append((number, headers, row))
                except StopIteration:
                    break

    def __extract_headers(self):

        # Extract headers
        keyed_source = False
        if self.__headers_row:
            for number, headers, row in self.__sample_extended_rows:
                if number == self.__headers_row:
                    if headers is not None:
                        self.__headers = headers
                        keyed_source = True
                    else:
                        self.__headers = row
            if not keyed_source:
                del self.__sample_extended_rows[:self.__headers_row]

    def __detect_html(self):

        # Detect html content
        text = ''
        for number, headers, row in self.__sample_extended_rows:
            for value in row:
                if isinstance(value, six.string_types):
                    text += value
        html_source = helpers.detect_html(text)
        if html_source:
            msg = 'Source has been detected as HTML (not supported)'
            raise exceptions.TabulatorException(msg)

    def __apply_processors(self, iterator):

        # Apply processors to iterator
        def builtin_processor(extended_rows):
            for number, headers, row in extended_rows:
                headers = self.__headers
                yield (number, headers, row)
        processors = [builtin_processor] + self.__post_parse
        for processor in processors:
            iterator = processor(iterator)
        return iterator


# Internal

_LOADERS = {
    'file': loaders.File,
    'stream': loaders.Stream,
    'text': loaders.Text,
    'ftp': loaders.Web,
    'ftps': loaders.Web,
    'http': loaders.Web,
    'https': loaders.Web,
    'native': loaders.Native,
}

_PARSERS = {
    'csv': parsers.CSV,
    'tsv': parsers.TSV,
    'xls': parsers.Excel,
    'xlsx': parsers.Excelx,
    'json': parsers.JSON,
    'native': parsers.Native,
}

_WRITERS = {
    'csv': writers.CSV,
}
