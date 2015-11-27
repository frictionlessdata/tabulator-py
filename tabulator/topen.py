from six.moves.urllib.parse import urlparse
from .table import Table
from . import loaders, parsers


LOADERS = {
    'file': loaders.File,
    'ftp': loaders.Web,
    'ftps': loaders.Web,
    'http': loaders.Web,
    'https': loaders.Web,
}

PARSERS = {
    'csv': parsers.CSV,
    'excel': parsers.Excel,
    'json': parsers.JSON,
}


def topen(source, encoding, format):
    """Open table from source with encoding and format.

    Args:

        source (str): source to source
            - file
            - web (http(s), ftp(s))

        encoding (str): encoding of source
            - auto
            - utf-8

        format (str): format of source
            - csv
            - json [not implemented]
            - excel [not implemented]

    """
    # TODO: implement error handling
    scheme = urlparse(source).scheme or 'file'
    loader = LOADERS[scheme](source, encoding)
    parser = PARSERS[format]()
    table = Table(loader=loader, parser=parser)
    table.open()
    return table
