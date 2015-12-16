# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

from .table import Table
from . import loaders, parsers, errors, helpers


DEFAULT_SCHEME = 'file'

LOADERS = {
    'file': loaders.File,
    'text': loaders.Text,
    'ftp': loaders.Web,
    'ftps': loaders.Web,
    'http': loaders.Web,
    'https': loaders.Web,
}

PARSERS = {
    'csv': parsers.CSV,
    'xls': parsers.Excel,
    'xlsx': parsers.Excel,
    'json': parsers.JSON,
}


def topen(source,
          scheme=None, format=None, encoding=None,
          loader_options=None, parser_options=None,
          loader_class=None, parser_class=None):
    """Open table from source with scheme, encoding and format.

    Function `topen` is a wrapper around `Table` interface.

    Parameters
    ----------
    source: str
        Path of contents.
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

    # Get loader
    if loader_class is None:
        if scheme is None:
            scheme = helpers.detect_scheme(source) or DEFAULT_SCHEME
        if scheme not in LOADERS:
            message = 'Scheme "%s" is not supported' % scheme
            raise errors.Error(message)
        loader_class = LOADERS[scheme]
    loader = loader_class(source, encoding, **loader_options)

    # Get parser
    if parser_class is None:
        if format is None:
            format = helpers.detect_format(source)
        if format not in PARSERS:
            message = 'Format "%s" is not supported' % format
            raise errors.Error(message)
        parser_class = PARSERS[format]
    parser = parser_class(**parser_options)

    # Initiate and open table
    table = Table(loader=loader, parser=parser)
    table.open()

    return table
