import io
from .api import API


class Text(API):
    """Loader to load source from text.
    """

    # Public

    def __init__(self, source, encoding=None):
        schema = 'text://'
        if source.startswith(schema):
            source = source.replace(schema, '', 1)
        if encoding is None:
            encoding = 'utf-8'
        self.__source = source
        self.__encoding = encoding

    def load(self, mode):
        bytes = io.BufferedRandom(io.BytesIO())
        bytes.write(self.__source.encode(self.__encoding))
        bytes.seek(0)
        if mode == 'b':
            return bytes
        elif mode == 't':
            chars = io.TextIOWrapper(bytes, self.__encoding)
            return chars
        else:
            message = 'Mode %s is not supported' % mode
            raise RuntimeError(message)

    @property
    def encoding(self):
        return self.__encoding
