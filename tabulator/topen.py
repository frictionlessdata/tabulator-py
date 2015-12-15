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
          loader_options=None, parser_options=None):
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

    # Get scheme, format
    if scheme is None:
        scheme = helpers.detect_scheme(source) or DEFAULT_SCHEME
    if format is None:
        format = helpers.detect_format(source)

    # Lookup and initiate loader
    if scheme not in LOADERS:
        message = 'Scheme "%s" is not supported' % scheme
        raise errors.Error(message)
    loader = LOADERS[scheme](source, encoding, **loader_options)

    # Lookup and initiate parser
    if format not in PARSERS:
        message = 'Format "%s" is not supported' % format
        raise errors.Error(message)
    parser = PARSERS[format]()

    # Initiate, open table
    table = Table(loader=loader, parser=parser, **parser_options)
    table.open()

    return table
