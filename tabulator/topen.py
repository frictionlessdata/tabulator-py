# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import warnings
from .table import Table
from . import exceptions
from . import helpers
from . import loaders
from . import parsers


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
    """Open table from source.

    Args:
        source (str): table source
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

    Returns:
        table (Table): opened table instance

    """
    # Initiate if None
    if loader_options is None:
        loader_options = {}
    if parser_options is None:
        parser_options = {}
    if post_parse is None:
        post_parse = []
    if sample_size is None:
        sample_size = _DEFAULT_SAMPLE_SIZE

    # DEPRECATED [v0.5-v1)
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

    # Get loader
    loader_constructor = loader_options.pop('constructor', None)
    if loader_constructor is None:
        if scheme is None:
            scheme = helpers.detect_scheme(source) or _DEFAULT_SCHEME
        if scheme not in _LOADERS:
            message = 'Scheme "%s" is not supported' % scheme
            raise exceptions.LoadingError(message)
        loader_constructor = _LOADERS[scheme]
    loader = loader_constructor(**loader_options)

    # Get parser
    parser_constructor = parser_options.pop('constructor', None)
    if parser_constructor is None:
        if format is None:
            format = helpers.detect_format(source)
        if format not in _PARSERS:
            message = 'Format "%s" is not supported' % format
            raise exceptions.ParsingError(message)
        parser_constructor = _PARSERS[format]
    parser = parser_constructor(**parser_options)

    # Initiate and open table
    table = Table(
        source, headers, encoding,
        post_parse=post_parse,
        sample_size=sample_size,
        loader=loader,
        parser=parser)
    table.open()

    return table


# Internal

_DEFAULT_SCHEME = 'file'
_DEFAULT_SAMPLE_SIZE = 100

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
