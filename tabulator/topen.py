from .table import Table
from . import loaders, parsers


LOADERS = {
    'file': loaders.File,
    'ftp': loaders.FTP,
    'http': loaders.HTTP,
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
            - http [not implemented]
            - ftp [not implemented]

        encoding (str): encoding of source
            - auto
            - utf-8

        format (str): format of source
            - csv
            - json [not implemented]
            - excel [not implemented]

    """
    # TODO: implement diff loaders
    # TODO: implement error handling
    loader = LOADERS['file'](path)
    parser = PARSERS[format](encoding)
    table = Table(loader=loader, parser=parser)
    table.open()
    return table
