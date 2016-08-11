# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

from .table import Table
from .processors import Headers
from . import loaders
from . import parsers
from . import errors
from . import helpers


# Module API

def topen(source,
          scheme=None,
          format=None,
          encoding=None,
          loader_options=None,
          parser_options=None,
          processors=None,
          with_headers=False):
    """Open table from source.

    Args:
        source (str): table source
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
        loader_options (dict):
            loader options:
                `constructor`: constructor returning `loaders.API` instance
                `encoding`: encoding of source
                <backend options>
        parser_options (dict):
            parser options:
                `constructor`: constructor returning `parsers.API` instance
                <backend options>
        processors (list): processors to add to the pipeline
        with_headers (bool): extract headers

    Returns:
        table (Table): opened table instance

    """
    # Initiate if None
    if loader_options is None:
        loader_options = {}
    if parser_options is None:
        parser_options = {}

    # Get loader
    loader_constructor = loader_options.pop('constructor', None)
    if loader_constructor is None:
        if scheme is None:
            scheme = helpers.detect_scheme(source) or _DEFAULT_SCHEME
        if scheme not in _LOADERS:
            message = 'Scheme "%s" is not supported' % scheme
            raise errors.Error(message)
        loader_constructor = _LOADERS[scheme]
    loader = loader_constructor(**loader_options)

    # Get parser
    parser_constructor = parser_options.pop('constructor', None)
    if parser_constructor is None:
        if format is None:
            format = helpers.detect_format(source)
        if format not in _PARSERS:
            message = 'Format "%s" is not supported' % format
            raise errors.Error(message)
        parser_constructor = _PARSERS[format]
    parser = parser_constructor(**parser_options)

    # Initiate and open table
    table = Table(source, encoding, loader=loader, parser=parser)
    table.open()

    # Add headers processor
    if with_headers:
        table.add_processor(Headers())

    # Add user processors
    if processors is not None:
        for processor in processors:
            table.add_processor(processor)

    return table


# Internal

_DEFAULT_SCHEME = 'file'

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
