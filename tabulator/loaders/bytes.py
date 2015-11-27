import io
from .api import API


class Bytes(API):
    """Loader to load source from bytes.
    """

    # Public

    def __init__(self, source, encoding):
        # TODO: add string suppport
        self.__source = source
        self.__encoding = encoding

    def load(self, mode):
        bytes = io.BufferedRandom(io.BytesIO())
        bytes.write(self.__source)
        bytes.seek(0)
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
