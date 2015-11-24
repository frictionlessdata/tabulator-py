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


def topen(path, encoding, format):
    """Open table from path with encoding and format.

    Args:

        path (str): path to source
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
    scheme = urlparse(path).scheme or 'file'
    loader = LOADERS[scheme](path)
    parser = PARSERS[format](encoding)
    table = Table(loader=loader, parser=parser)
    table.open()
    return table
