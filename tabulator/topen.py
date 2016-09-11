# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import six
import warnings
from .stream import Stream


# Module API

def topen(source,
          headers=None,
          scheme=None,
          format=None,
          encoding=None,
          post_parse=None,
          sample_size=None,
          loader_options=None,
          parser_options=None,
          # DEPRECATED [v0.5-v1)
          loader_class=None,
          parser_class=None,
          with_headers=False,
          extract_headers=False):
    """Open stream from source.

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
        sample_size (int): rows count for stream.sample. Set to "0" to prevent
            any parsing activities before actual stream.iter call. In this case
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

    Returns:
        stream (Stream): opened stream instance

    """

    # DEPRECATED [v0.5-v1)
    if loader_options is None:
        loader_options = {}
    if parser_options is None:
        parser_options = {}
    if loader_class is not None:
        message = 'Argument "loaders_class" is deprecated [v0.5-v1)'
        warnings.warn(message, UserWarning)
        loader_options['constructor'] = loader_class
    if parser_class is not None:
        message = 'Argument "parser_class" is deprecated [v0.5-v1)'
        warnings.warn(message, UserWarning)
        parser_options['constructor'] = parser_class
    if with_headers:
        message = 'Argument "with_headers" is deprecated [v0.5-v1)'
        warnings.warn(message, UserWarning)
        headers = 'row1'
    if extract_headers:
        message = 'Argument "extract_headers" is deprecated [v0.5-v1)'
        warnings.warn(message, UserWarning)
        headers = 'row1'

    # DEPRECATED [v0.6-v1)
    message = 'Function "topen" is deprecated [v0.6-v1)'
    warnings.warn(message, UserWarning)
    if 'constructor' in loader_options:
        message = 'Argument "constructor" is deprecated [v0.6-v1)'
        warnings.warn(message, UserWarning)
        loader_options.pop('constructor', None)
    if 'constructor' in parser_options:
        message = 'Argument "constructor" is deprecated [v0.6-v1)'
        warnings.warn(message, UserWarning)
        parser_options.pop('constructor', None)
    if isinstance(headers, six.string_types):
        message = 'Headers like "row1" is deprecated [v0.6-v1)'
        warnings.warn(message, UserWarning)
        headers = int(headers.replace('row', ''))

    # Initiate and open stream
    stream = Stream(
        source, headers, scheme, format, encoding,
        post_parse=post_parse,
        sample_size=sample_size,
        loader_options=loader_options,
        parser_options=parser_options)
    stream.open()

    return stream
