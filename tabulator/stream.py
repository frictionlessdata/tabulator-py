# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import six
import warnings
from copy import copy
from itertools import chain
from . import exceptions
from . import helpers
from . import config


# Module API

class Stream(object):
    """Tabular stream.

    Args:
        source (str): stream source
        headers (list/str):
            headers list or pointer:
                - list of headers for setting by user
                - row number to extract headers from this row
                  For plain source headers row and all rows
                  before will be removed. For keyed source no rows
                  will be removed.
        scheme (str):
            scheme of source:
                - file (default)
                - ftp
                - ftps
                - gsheet
                - http
                - https
                - native
                - stream
                - text
        format (str):
            format of source:
                - None (detect)
                - csv
                  options:
                    - delimiter
                    - doublequote
                    - escapechar
                    - quotechar
                    - quoting
                    - skipinitialspace
                - gsheet
                - json
                  options:
                    - prefix
                - native
                - tsv
                - xls
                  options:
                    - sheet
                - xlsx
                  options:
                    - sheet
        encoding (str):
            encoding of source:
                - None (detect)
                - utf-8
                - <encodings>
        sample_size (int): rows count for table.sample. Set to "0" to prevent
            any parsing activities before actual table.iter call. In this case
            headers will not be extracted from the source.
        post_parse (generator[]): post parse processors (hooks). Signature
            to follow is "processor(extended_rows)" which should yield
            one extended row (number, headers, row) per yield instruction.
        options (dict): see in the scheme/format section

    """

    # Public

    def __init__(self,
                 source,
                 headers=None,
                 scheme=None,
                 format=None,
                 encoding=None,
                 sample_size=100,
                 post_parse=[],
                 # DEPRECATED [v0.8-v1)
                 loader_options={},
                 parser_options={},
                 **options):

        # DEPRECATED [v0.8-v1)
        if loader_options:
            options.update(loader_options)
            message = 'Use kwargs instead of "loader_options"'
            warnings.warn(message, UserWarning)
        if parser_options is None:
            options.update(parser_options)
            message = 'Use kwargs instead of "parser_options"'
            warnings.warn(message, UserWarning)

        # Set headers
        self.__headers = None
        self.__headers_row = 0
        if isinstance(headers, (tuple, list)):
            self.__headers = list(headers)
        elif isinstance(headers, int):
            self.__headers_row = headers

        # Set attributes
        self.__source = source
        self.__scheme = scheme
        self.__format = format
        self.__encoding = encoding
        self.__post_parse = copy(post_parse)
        self.__sample_size = sample_size
        self.__options = options
        self.__sample_extended_rows = []
        self.__loader = None
        self.__parser = None
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
        return not self.__parser or self.__parser.closed

    def open(self):
        """Open table to iterate over it.
        """

        # Prepare variables
        scheme = self.__scheme
        format = self.__format
        options = copy(self.__options)

        # Initiate loader
        self.__loader = None
        if scheme is None:
            scheme = helpers.detect_scheme(self.__source)
            if not scheme:
                scheme = config.DEFAULT_SCHEME
        if scheme not in config.LOADERS:
            message = 'Scheme "%s" is not supported' % scheme
            raise exceptions.SchemeError(message)
        loader_path = config.LOADERS[scheme]
        if loader_path:
            loader_class = helpers.import_attribute(loader_path)
            loader_options = helpers.extract_options(options, loader_class.options)
            self.__loader = loader_class(**loader_options)

        # Initiate parser
        if format is None:
            format = helpers.detect_format(self.__source)
        if format not in config.PARSERS:
            message = 'Format "%s" is not supported' % format
            raise exceptions.FormatError(message)
        parser_class = helpers.import_attribute(config.PARSERS[format])
        parser_options = helpers.extract_options(options, parser_class.options)
        self.__parser = parser_class(**parser_options)

        # Bad options
        if options:
            message = 'Not supported options "%s" for scheme "%s" and format "%s"'
            message = message % (', '.join(options), scheme, format)
            raise exceptions.OptionsError(message)

        # Open and setup
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

    def save(self, target, format=None,  encoding=None, **options):
        """Save stream to filesystem.

        Args:
            target (str): stream target
            format (str):
                saving format:
                    - None (detect)
                    - csv
                      options:
                        - delimiter
            encoding (str):
                saving encoding:
                    - utf-8 (default)
                    - <encodings>

        """
        if encoding is None:
            encoding = config.DEFAULT_ENCODING
        if format is None:
            format = helpers.detect_format(target)
        if format not in config.WRITERS:
            message = 'Format "%s" is not supported' % format
            raise exceptions.FormatError(message)
        extended_rows = self.iter(extended=True)
        writer_class = helpers.import_attribute(config.WRITERS[format])
        writer_options = helpers.extract_options(options, writer_class.options)
        if options:
            message = 'Not supported options "%s" for format "%s"'
            message = message % (', '.join(options), format)
            raise exceptions.OptionsError(message)
        writer = writer_class(**writer_options)
        writer.write(target, encoding, extended_rows)

    @staticmethod
    def test(source, scheme=None, format=None):
        """Test if this source has supported scheme and format.

        Args:
            source (str): stream source
            scheme (str): stream scheme
            format (str): stream format

        Returns:
            bool: True if source source has supported scheme and format

        """
        if scheme is None:
            scheme = helpers.detect_scheme(source)
            if not scheme:
                scheme = config.DEFAULT_SCHEME
        if scheme not in config.LOADERS:
            return False
        if format is None:
            format = helpers.detect_format(source)
        if format not in config.PARSERS:
            return False
        return True

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
            if self.__headers_row > self.__sample_size:
                message = 'Headers row (%s) can\'t be more than sample_size (%s)'
                message = message % (self.__headers_row, self.__sample_size)
                raise exceptions.OptionsError(message)
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
            message = 'Format has been detected as HTML (not supported)'
            raise exceptions.FormatError(message)

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
