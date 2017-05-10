# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import six
from copy import copy
from itertools import chain
from . import exceptions
from . import helpers
from . import config


# Module API

class Stream(object):

    # Public

    def __init__(self,
                 source,
                 headers=None,
                 scheme=None,
                 format=None,
                 encoding=None,
                 sample_size=100,
                 allow_html=False,
                 force_strings=False,
                 force_parse=False,
                 skip_rows=[],
                 post_parse=[],
                 custom_loaders={},
                 custom_parsers={},
                 custom_writers={},
                 **options):
        """https://github.com/frictionlessdata/tabulator-py#stream
        """

        # Set headers
        self.__headers = None
        self.__headers_row = 0
        if isinstance(headers, (tuple, list)):
            self.__headers = list(headers)
        elif isinstance(headers, int):
            self.__headers_row = headers

        # Set skip rows
        self.__skip_rows_by_numbers = []
        self.__skip_rows_by_comments = []
        for directive in copy(skip_rows):
            if isinstance(directive, int):
                self.__skip_rows_by_numbers.append(directive)
            else:
                self.__skip_rows_by_comments.append(str(directive))

        # Set attributes
        self.__source = source
        self.__scheme = scheme
        self.__format = format
        self.__encoding = encoding
        self.__sample_size = sample_size
        self.__allow_html = allow_html
        self.__force_strings = force_strings
        self.__force_parse = force_parse
        self.__post_parse = copy(post_parse)
        self.__custom_loaders = copy(custom_loaders)
        self.__custom_parsers = copy(custom_parsers)
        self.__custom_writers = copy(custom_writers)
        self.__options = options
        self.__sample_extended_rows = []
        self.__loader = None
        self.__parser = None
        self.__row_number = 0

    def __enter__(self):
        """https://github.com/frictionlessdata/tabulator-py#stream
        """
        if self.closed:
            self.open()
        return self

    def __exit__(self, type, value, traceback):
        """https://github.com/frictionlessdata/tabulator-py#stream
        """
        if not self.closed:
            self.close()

    def __iter__(self):
        """https://github.com/frictionlessdata/tabulator-py#stream
        """
        return self.iter()

    @property
    def closed(self):
        """https://github.com/frictionlessdata/tabulator-py#stream
        """
        return not self.__parser or self.__parser.closed

    def open(self):
        """https://github.com/frictionlessdata/tabulator-py#stream
        """

        # Get scheme and format
        detected_scheme, detected_format = helpers.detect_scheme_and_format(self.__source)
        scheme = self.__scheme or detected_scheme
        format = self.__format or detected_format

        # Get options
        options = copy(self.__options)

        # Initiate loader
        self.__loader = None
        if scheme is not None:
            loader_class = self.__custom_loaders.get(scheme)
            if loader_class is None:
                if scheme not in config.LOADERS:
                    message = 'Scheme "%s" is not supported' % scheme
                    raise exceptions.SchemeError(message)
                loader_path = config.LOADERS[scheme]
                if loader_path:
                    loader_class = helpers.import_attribute(loader_path)
            if loader_class is not None:
                loader_options = helpers.extract_options(options, loader_class.options)
                self.__loader = loader_class(**loader_options)

        # Initiate parser
        parser_class = self.__custom_parsers.get(format)
        if parser_class is None:
            if format not in config.PARSERS:
                message = 'Format "%s" is not supported' % format
                raise exceptions.FormatError(message)
            parser_class = helpers.import_attribute(config.PARSERS[format])
        parser_options = helpers.extract_options(options, parser_class.options)
        self.__parser = parser_class(self.__loader, **parser_options)

        # Bad options
        if options:
            message = 'Not supported options "%s" for scheme "%s" and format "%s"'
            message = message % (', '.join(options), scheme, format)
            raise exceptions.OptionsError(message)

        # Open and setup
        self.__parser.open(
            self.__source, encoding=self.__encoding, force_parse=self.__force_parse)
        self.__extract_sample()
        self.__extract_headers()
        if not self.__allow_html:
            self.__detect_html()

        return self

    def close(self):
        """https://github.com/frictionlessdata/tabulator-py#stream
        """
        self.__parser.close()

    def reset(self):
        """https://github.com/frictionlessdata/tabulator-py#stream
        """
        if self.__row_number > self.__sample_size:
            self.__parser.reset()
            self.__extract_sample()
            self.__extract_headers()
        self.__row_number = 0

    @property
    def headers(self):
        """https://github.com/frictionlessdata/tabulator-py#stream
        """
        return self.__headers

    @property
    def sample(self):
        """https://github.com/frictionlessdata/tabulator-py#stream
        """
        sample = []
        iterator = iter(self.__sample_extended_rows)
        iterator = self.__apply_processors(iterator)
        for row_number, headers, row in iterator:
            sample.append(row)
        return sample

    def iter(self, keyed=False, extended=False):
        """https://github.com/frictionlessdata/tabulator-py#stream
        """
        iterator = chain(
            self.__sample_extended_rows,
            self.__parser.extended_rows)
        iterator = self.__apply_processors(iterator)
        for row_number, headers, row in iterator:
            if self.__force_strings:
                row = list(map(helpers.stringify_value, row))
            if row_number > self.__row_number:
                self.__row_number = row_number
                if extended:
                    yield (row_number, headers, row)
                elif keyed:
                    yield dict(zip(headers, row))
                else:
                    yield row

    def read(self, keyed=False, extended=False, limit=None):
        """https://github.com/frictionlessdata/tabulator-py#stream
        """
        result = []
        rows = self.iter(keyed=keyed, extended=extended)
        for count, row in enumerate(rows, start=1):
            result.append(row)
            if count == limit:
                break
        return result

    def save(self, target, format=None,  encoding=None, **options):
        """https://github.com/frictionlessdata/tabulator-py#stream
        """
        if encoding is None:
            encoding = config.DEFAULT_ENCODING
        if format is None:
            _, format = helpers.detect_scheme_and_format(target)
        writer_class = self.__custom_writers.get(format)
        if writer_class is None:
            if format not in config.WRITERS:
                message = 'Format "%s" is not supported' % format
                raise exceptions.FormatError(message)
            writer_class = helpers.import_attribute(config.WRITERS[format])
        writer_options = helpers.extract_options(options, writer_class.options)
        if options:
            message = 'Not supported options "%s" for format "%s"'
            message = message % (', '.join(options), format)
            raise exceptions.OptionsError(message)
        writer = writer_class(**writer_options)
        writer.write(self.iter(), target, headers=self.headers, encoding=encoding)

    # Private

    def __extract_sample(self):

        # Extract sample
        self.__sample_extended_rows = []
        if self.__sample_size:
            for _ in range(self.__sample_size):
                try:
                    row_number, headers, row = next(self.__parser.extended_rows)
                    self.__sample_extended_rows.append((row_number, headers, row))
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
            for row_number, headers, row in self.__sample_extended_rows:
                if row_number == self.__headers_row:
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
        for row_number, headers, row in self.__sample_extended_rows:
            for value in row:
                if isinstance(value, six.string_types):
                    text += value
        html_source = helpers.detect_html(text)
        if html_source:
            message = 'Format has been detected as HTML (not supported)'
            raise exceptions.FormatError(message)

    def __apply_processors(self, iterator):

        # Builtin processor
        def builtin_processor(extended_rows):
            for row_number, headers, row in extended_rows:
                # Set headers
                headers = self.__headers
                # Skip row by numbers
                if row_number in self.__skip_rows_by_numbers:
                    continue
                # Skip row by comments
                match = lambda comment: row[0].startswith(comment)
                if list(filter(match, self.__skip_rows_by_comments)):
                    continue
                yield (row_number, headers, row)

        # Apply processors to iterator
        processors = [builtin_processor] + self.__post_parse
        for processor in processors:
            iterator = processor(iterator)
        return iterator
