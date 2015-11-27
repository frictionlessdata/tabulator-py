import io
from .api import API


class File(API):
    """Loader to load source from filesystem.
    """

    # Public

    def __init__(self, source, encoding):
        schema = 'file://'
        if source.startswith(schema):
            source = source.replace(schema, '', 1)
        self.__source = source
        self.__encoding = encoding

    def load(self, mode):
        bytes = io.open(self.__source, 'rb')
        if mode == 't':
            chars = io.TextIOWrapper(bytes, self.__encoding)
            return chars
        elif mode == 'b':
            return bytes
        else:
            message = 'Mode %s is not supported' % mode
            raise RuntimeError(message)

    @property
    def encoding(self):
        return self.__encoding
