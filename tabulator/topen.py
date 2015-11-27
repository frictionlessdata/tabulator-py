from six.moves.urllib.parse import urlparse
from .table import Table
from . import loaders, parsers


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
    'excel': parsers.Excel,
    'json': parsers.JSON,
}


def topen(source, encoding=None, format=None):
    """Open table from source with encoding and format.

    Args:

        source (str): source to source
            - file
            - text
            - web (http(s), ftp(s))

        encoding (str): encoding of source
            - utf-8 [default]
            - infer
            - <any>

        format (str): format of source
            - csv [default]
            - json
            - excel

    """
    # TODO: implement error handling
    scheme = urlparse(source).scheme or 'file'
    loader = LOADERS[scheme](source, encoding)
    parser = PARSERS[format]()
    table = Table(loader=loader, parser=parser)
    table.open()
    return table
