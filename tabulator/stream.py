# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import six
import gzip
import zipfile
import tempfile
import warnings
from copy import copy
from itertools import chain
from collections import deque
from .loaders.stream import StreamLoader
from . import exceptions
from . import helpers
from . import config


# Module API

class Stream(object):
    '''Stream of tabular data.

    This is the main `tabulator` class. It loads a data source, and allows you
    to stream its parsed contents.

    Args:
        source (str): Path to file as ``<scheme>://path/to/file.<format>``. If
            not explicitly set, the scheme (file, http, ...) and format (csv, xls,
            ...) are inferred from the source string.
        headers (Union[int, List[int], List[str]], optional): Either a row
            number or list of row numbers (in case of multi-line headers) to be
            considered as headers (rows start counting at 1), or the actual
            headers defined a list of strings. If not set, all rows will be
            treated as containing values.
        scheme (str, optional): Scheme for loading the file (file, http, ...).
             If not set, it'll be inferred from `source`.
        format (str, optional): File source's format (csv, xls, ...). If not
             set, it'll be inferred from `source`. inferred
        encoding (str, optional): Source encoding. If not set, it'll be inferred.
        compression (str, optional): Source file compression (zip, ...). If not
            set, it'll be inferred.
        allow_html (bool, optional): Allow the file source to be an HTML page.
            If False, raises ``exceptions.FormatError`` if the loaded file is
            an HTML page. Defaults to False.
        sample_size (int, optional): Controls the number of sample rows used to
            infer properties from the data (headers, encoding, etc.). Set to
            ``0`` to disable sampling, in which case nothing will be inferred
            from the data. Defaults to ``config.DEFAULT_SAMPLE_SIZE``.
        bytes_sample_size (int, optional): Same as `sample_size`, but instead
            of number of rows, controls number of bytes. Defaults to
            ``config.DEFAULT_BYTES_SAMPLE_SIZE``.
        ignore_blank_headers (bool, optional): When True, ignores all columns
            that have blank headers. Defaults to False.
        force_strings (bool, optional): When True, casts all data to strings.
            Defaults to False.
        force_parse (bool, optional): When True, don't raise exceptions when
            parsing malformed rows, simply returning an empty value. Defaults
            to False.
        skip_rows (List[Union[int, str]], optional): List of row numbers and
            strings to skip. If a string, it'll skip rows that begin with it
            (e.g. '#' and '//').
        post_parse (List[function], optional): List of generator functions that
            receives a list of rows and headers, processes them, and yields
            them (or not). Useful to pre-process the data. Defaults to None.
        custom_loaders (dict, optional): Dictionary with keys as scheme names,
            and values as their respective ``Loader`` class implementations.
            Defaults to None.
        custom_parsers (dict, optional): Dictionary with keys as format names,
            and values as their respective ``Parser`` class implementations.
            Defaults to None.
        custom_loaders (dict, optional): Dictionary with keys as writer format
            names, and values as their respective ``Writer`` class
            implementations. Defaults to None.
        **options (Any, optional): Extra options passed to the loaders and parsers.

    Returns:
        Stream: The Stream instance.
    '''

    # Public

    def __init__(self,
                 source,
                 headers=None,
                 scheme=None,
                 format=None,
                 encoding=None,
                 compression=None,
                 allow_html=False,
                 sample_size=config.DEFAULT_SAMPLE_SIZE,
                 bytes_sample_size=config.DEFAULT_BYTES_SAMPLE_SIZE,
                 ignore_blank_headers=False,
                 force_strings=False,
                 force_parse=False,
                 skip_rows=[],
                 post_parse=[],
                 custom_loaders={},
                 custom_parsers={},
                 custom_writers={},
                 **options):

        # Set headers
        self.__headers = None
        self.__headers_row = None
        self.__headers_row_last = None
        if isinstance(headers, int):
            self.__headers_row = headers
            self.__headers_row_last = headers
        elif isinstance(headers, (tuple, list)):
            if (len(headers) == 2 and
                    isinstance(headers[0], int) and
                    isinstance(headers[1], int)):
                self.__headers_row = headers[0]
                self.__headers_row_last = headers[1]
            else:
                self.__headers = list(headers)

        # Set skip rows
        self.__skip_rows_by_numbers = []
        self.__skip_rows_by_comments = []
        for directive in copy(skip_rows):
            if isinstance(directive, int):
                self.__skip_rows_by_numbers.append(directive)
            else:
                self.__skip_rows_by_comments.append(str(directive))

        # Support for pathlib.Path
        if hasattr(source, 'joinpath'):
            source = str(source)

        # Set attributes
        self.__source = source
        self.__scheme = scheme
        self.__format = format
        self.__encoding = encoding
        self.__compression = compression
        self.__allow_html = allow_html
        self.__sample_size = sample_size
        self.__bytes_sample_size = bytes_sample_size
        self.__ignore_blank_headers = ignore_blank_headers
        self.__blank_header_indexes = []
        self.__force_strings = force_strings
        self.__force_parse = force_parse
        self.__post_parse = copy(post_parse)
        self.__custom_loaders = copy(custom_loaders)
        self.__custom_parsers = copy(custom_parsers)
        self.__custom_writers = copy(custom_writers)
        self.__actual_scheme = scheme
        self.__actual_format = format
        self.__actual_encoding = encoding
        self.__options = options
        self.__sample_extended_rows = []
        self.__loader = None
        self.__parser = None
        self.__row_number = 0

    def __enter__(self):
        if self.closed:
            self.open()
        return self

    def __exit__(self, type, value, traceback):
        if not self.closed:
            self.close()

    def __iter__(self):
        return self.iter()

    @property
    def closed(self):
        '''Returns True if the underlying stream is closed, False otherwise.'''
        return not self.__parser or self.__parser.closed

    def open(self):
        '''Opens the stream for reading.'''
        options = copy(self.__options)

        # Get scheme and format
        detected_scheme, detected_format = helpers.detect_scheme_and_format(self.__source)
        scheme = self.__scheme or detected_scheme
        format = self.__format or detected_format

        # Get compression
        compression = None
        for type in config.SUPPORTED_COMPRESSION:
            if self.__compression == type or detected_format == type:
                compression = type

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
                if compression and 'http_stream' in loader_class.options:
                    loader_options['http_stream'] = False
                self.__loader = loader_class(
                    bytes_sample_size=self.__bytes_sample_size,
                    **loader_options)

        # Zip compression
        if compression == 'zip' and six.PY3:
            source = self.__loader.load(self.__source, mode='b')
            with zipfile.ZipFile(source) as archive:
                name = archive.namelist()[0]
                with archive.open(name) as file:
                    source = tempfile.NamedTemporaryFile(suffix='.' + name)
                    for line in file:
                        source.write(line)
                    source.seek(0)
            self.__source = source
            self.__loader = StreamLoader(bytes_sample_size=self.__bytes_sample_size)
            format = self.__format or helpers.detect_scheme_and_format(source.name)[1]
            scheme = 'stream'

        # Gzip compression
        elif compression == 'gz' and six.PY3:
            name = self.__source.replace('.gz', '')
            self.__source = gzip.open(self.__loader.load(self.__source, mode='b'))
            self.__loader = StreamLoader(bytes_sample_size=self.__bytes_sample_size)
            format = self.__format or helpers.detect_scheme_and_format(name)[1]
            scheme = 'stream'

        # Not supported compression
        elif compression:
            message = 'Compression "%s" is not supported for your Python version'
            raise exceptions.TabulatorException(message % compression)

        # Initiate parser
        parser_class = self.__custom_parsers.get(format)
        if parser_class is None:
            if format not in config.PARSERS:
                message = 'Format "%s" is not supported' % format
                raise exceptions.FormatError(message)
            parser_class = helpers.import_attribute(config.PARSERS[format])
        parser_options = helpers.extract_options(options, parser_class.options)
        self.__parser = parser_class(self.__loader,
                force_parse=self.__force_parse,
                **parser_options)

        # Bad options
        if options:
            message = 'Not supported option(s) "%s" for scheme "%s" and format "%s"'
            message = message % (', '.join(options), scheme, format)
            warnings.warn(message, UserWarning)

        # Open and setup
        self.__parser.open(self.__source, encoding=self.__encoding)
        self.__extract_sample()
        self.__extract_headers()
        if not self.__allow_html:
            self.__detect_html()

        # Set scheme/format/encoding
        self.__actual_scheme = scheme
        self.__actual_format = format
        self.__actual_encoding = self.__parser.encoding

        return self

    def close(self):
        '''Closes the stream.'''
        self.__parser.close()
        self.__row_number = 0

    def reset(self):
        '''Resets the stream pointer to the beginning of the file.'''
        if self.__row_number > self.__sample_size:
            self.__parser.reset()
            self.__extract_sample()
            self.__extract_headers()
        self.__row_number = 0

    @property
    def headers(self):
        return self.__headers

    @property
    def scheme(self):
        return self.__actual_scheme

    @property
    def format(self):
        return self.__actual_format

    @property
    def encoding(self):
        return self.__actual_encoding

    @property
    def sample(self):
        '''Returns the stream's rows used as sample.

        These sample rows are used internally to infer characteristics of the
        source file (e.g. encoding, headers, ...).
        '''
        sample = []
        iterator = iter(self.__sample_extended_rows)
        iterator = self.__apply_processors(iterator)
        for row_number, headers, row in iterator:
            sample.append(row)
        return sample

    def iter(self, keyed=False, extended=False):
        '''Iterate over the rows.

        Each row is returned in a format that depends on the arguments `keyed`
        and `extended`. By default, each row is returned as list of their
        values.

        Args:
            keyed (bool, optional): When True, each returned row will be a
                `dict` mapping the header name to its value in the current row.
                For example, `[{'name': 'J Smith', 'value': '10'}]`. Ignored if
                ``extended`` is True. Defaults to False.
            extended (bool, optional): When True, returns each row as a tuple
                with row number (starts at 1), list of headers, and list of row
                values. For example, `(1, ['name', 'value'], ['J Smith', '10'])`.
                Defaults to False.

        Returns:
            Iterator[Union[List[Any], Dict[str, Any], Tuple[int, List[str], List[Any]]]]:
                The row itself. The format depends on the values of `keyed` and
                `extended` arguments.

        Raises:
            exceptions.TabulatorException: If the stream is closed.
        '''

        # Error if closed
        if self.closed:
            message = 'Stream is closed. Please call "stream.open()" first.'
            raise exceptions.TabulatorException(message)

        # Create iterator
        iterator = chain(
            self.__sample_extended_rows,
            self.__parser.extended_rows)
        iterator = self.__apply_processors(iterator)

        # Yield rows from iterator
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
        '''Returns a list of rows.

        Args:
            keyed (bool, optional): See :func:`Stream.iter`.
            extended (bool, optional): See :func:`Stream.iter`.
            limit (int, optional): Number of rows to return. If None, returns
            all rows. Defaults to None.

        Returns:
            List[Union[List[Any], Dict[str, Any], Tuple[int, List[str], List[Any]]]]:
                The list of rows. The format depends on the values of `keyed`
                and `extended` arguments.
        '''
        result = []
        rows = self.iter(keyed=keyed, extended=extended)
        for count, row in enumerate(rows, start=1):
            result.append(row)
            if count == limit:
                break
        return result

    def save(self, target, format=None,  encoding=None, **options):
        '''Save stream to the local filesystem.

        Args:
            target (str): Path where to save the stream.
            format (str, optional): The format the stream will be saved as. If
                None, detects from the ``target`` path. Defaults to None.
            encoding (str, optional): Saved file encoding. Defaults to
                ``config.DEFAULT_ENCODING``.
            **options: Extra options passed to the writer.
        '''

        # Get encoding/format
        if encoding is None:
            encoding = config.DEFAULT_ENCODING
        if format is None:
            _, format = helpers.detect_scheme_and_format(target)

        # Prepare writer class
        writer_class = self.__custom_writers.get(format)
        if writer_class is None:
            if format not in config.WRITERS:
                message = 'Format "%s" is not supported' % format
                raise exceptions.FormatError(message)
            writer_class = helpers.import_attribute(config.WRITERS[format])

        # Prepare writer options
        writer_options = helpers.extract_options(options, writer_class.options)
        if options:
            message = 'Not supported options "%s" for format "%s"'
            message = message % (', '.join(options), format)
            raise exceptions.TabulatorException(message)

        # Write data to target
        writer = writer_class(**writer_options)
        writer.write(self.iter(), target, headers=self.headers, encoding=encoding)

    # Private

    def __extract_sample(self):

        # Sample is not requested
        if not self.__sample_size:
            return

        # Extract sample rows
        self.__sample_extended_rows = []
        for _ in range(self.__sample_size):
            try:
                row_number, headers, row = next(self.__parser.extended_rows)
                self.__sample_extended_rows.append((row_number, headers, row))
            except StopIteration:
                break

    def __extract_headers(self):

        # Heders row is not set
        if not self.__headers_row:
            return

        # Sample is too short
        if self.__headers_row > self.__sample_size:
            message = 'Headers row (%s) can\'t be more than sample_size (%s)'
            message = message % (self.__headers_row, self.__sample_size)
            raise exceptions.TabulatorException(message)

        # Get headers from data
        keyed_source = False
        for row_number, headers, row in self.__sample_extended_rows:
            keyed_source = keyed_source or headers is not None
            headers = headers if keyed_source else row
            for index, header in enumerate(headers):
                if header is not None:
                    headers[index] = six.text_type(header).strip()
            if row_number == self.__headers_row:
                self.__headers = headers
            if row_number > self.__headers_row:
                for index in range(0, len(self.__headers)):
                    if len(headers) > index and headers[index] is not None:
                        if not self.__headers[index]:
                            self.__headers[index] = headers[index]
                        elif not self.__headers[index].endswith(headers[index]):
                            self.__headers[index] += ' ' + headers[index]
            if row_number == self.__headers_row_last:
                break

        # Ignore blank headers
        if self.__ignore_blank_headers:
            self.__blank_header_indexes = []
            raw_headers, self.__headers = self.__headers, []
            for index, header in list(enumerate(raw_headers)):
                if header in ['', None]:
                    self.__blank_header_indexes.append(index)
                    continue
                self.__headers.append(header)
            self.__blank_header_indexes = sorted(self.__blank_header_indexes, reverse=True)

        # Remove headers from data
        if not keyed_source:
            del self.__sample_extended_rows[:self.__headers_row_last]

    def __detect_html(self):

        # Prepare text
        text = ''
        for row_number, headers, row in self.__sample_extended_rows:
            for value in row:
                if isinstance(value, six.string_types):
                    text += value

        # Detect html content
        html_source = helpers.detect_html(text)
        if html_source:
            message = 'Format has been detected as HTML (not supported)'
            raise exceptions.FormatError(message)

    def __apply_processors(self, iterator):

        # Base processor
        def builtin_processor(extended_rows):
            for row_number, headers, row in extended_rows:

                # Sync headers/row
                if headers != self.__headers:
                    if headers and self.__headers:
                        keyed_row = dict(zip(headers, row))
                        row = [keyed_row.get(header) for header in self.__headers]
                    headers = self.__headers

                # Skip row by numbers
                if row_number in self.__skip_rows_by_numbers:
                    continue

                # Skip row by comments
                match = lambda comment: (
                    (isinstance(row[0], six.string_types) and
                     row[0].startswith(comment)) if len(comment) > 0
                    else row[0] in ('', None)
                )
                if any(map(match, self.__skip_rows_by_comments)):
                    continue

                # Ignore blank headers
                if self.__blank_header_indexes:
                    for index in self.__blank_header_indexes:
                        if index < len(row):
                            row = row[:index] + row[index+1:]

                yield (row_number, headers, row)

        # Skip nagative rows processor
        def skip_negative_rows(extended_rows):
            '''
            This processor will skip rows which counts from the end, e.g.
            -1: skip last row, -2: skip pre-last row, etc.
            Rows to skip are taken from  Stream.__skip_rows_by_numbers
            '''
            rows_to_skip = [n for n in self.__skip_rows_by_numbers if n < 0]
            buffer_size = abs(min(rows_to_skip))
            # collections.deque - takes O[1] time to push/pop values from any side.
            buffer = deque()

            # use buffer to save last rows
            for row in extended_rows:
                buffer.append(row)
                if len(buffer) > buffer_size:
                    yield buffer.popleft()

            # Now squeeze out the buffer
            n = len(buffer)
            for i, row in enumerate(buffer):
                if i - n not in rows_to_skip:
                    yield row

        # Form a processors list
        processors = [builtin_processor]
        # if we have to delete some rows with negative index (counting from the end)
        if [n for n in self.__skip_rows_by_numbers if n < 0]:
            processors.insert(0, skip_negative_rows)
        if self.__post_parse:
            processors += self.__post_parse

        # Apply processors to iterator
        for processor in processors:
            iterator = processor(iterator)

        return iterator
