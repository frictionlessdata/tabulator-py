# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

from .table import Table
from .iterator import Iterator
from .processors import Headers
from . import loaders
from . import parsers
from . import errors
from . import helpers


# Module API

def topen(source,
          with_headers=False, processors=None,
          scheme=None, format=None, encoding=None,
          loader_options=None, parser_options=None,
          loader_class=None, parser_class=None,
          iterator_class=None,
          table_class=None):
    """Open table from source with scheme, encoding and format.

    Function `topen` is a wrapper around `Table` interface.

    Parameters
    ----------
    source: str
        Path of contents.
    with_headers: bool
        Extract headers.
    processors: list
        Processors to add to pipeline.
    scheme: str
        Scheme of source:
            - file (default)
            - text
            - http
            - https
            - ftp
            - ftps
    format: str
        Format of source:
            - None (detect)
            - csv
            - json
            - xls
            - xlsx
    encoding: str
        Encoding of source:
            - None (detect)
            - utf-8
            - <any>
    loader_options: dict
        Loader options.
    parser_options: dict
        Parser options.
    loader_class: type
        Loader class.
    parser_class: type
        Parser class.
    iterator_class: type
        Iterator class.
    table_class: type
        Table class.

    Returns
    -------
    table: `Table`
        Opened Table instance.

    """
    # Initiate if None
    if loader_options is None:
        loader_options = {}
    if parser_options is None:
        parser_options = {}
    if iterator_class is None:
        iterator_class = Iterator
    if table_class is None:
        table_class = Table

    # Get loader
    if loader_class is None:
        if scheme is None:
            scheme = helpers.detect_scheme(source) or _DEFAULT_SCHEME
        if scheme not in _LOADERS:
            message = 'Scheme "%s" is not supported' % scheme
            raise errors.Error(message)
        loader_class = _LOADERS[scheme]
    loader = loader_class(source, encoding, **loader_options)

    # Get parser
    if parser_class is None:
        if format is None:
            format = helpers.detect_format(source)
        if format not in _PARSERS:
            message = 'Format "%s" is not supported' % format
            raise errors.Error(message)
        parser_class = _PARSERS[format]
    parser = parser_class(**parser_options)

    # Initiate and open table
    table = table_class(
            loader=loader,
            parser=parser,
            iterator_class=iterator_class)
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
}

_PARSERS = {
    'csv': parsers.CSV,
    'xls': parsers.Excel,
    'xlsx': parsers.Excelx,
    'json': parsers.JSON,
}
