import io
from .api import API


class Text(API):
    """Loader to load source from text.
    """

    DEFAULT_ENCODING = 'utf-8'

    # Public

    def __init__(self, source, encoding=None):
        if encoding is None:
            encoding = 'utf-8'
        self.__source = source
        self.__encoding = encoding

    def load(self, mode):

        # Prepare source
        schema = 'text://'
        source = self.__source
        if source.startswith(schema):
            source = source.replace(schema, '', 1)

        # Prepare encoding
        encoding = self.DEFAULT_ENCODING
        if self.__encoding is not None:
            encoding = self.__encoding

        # Prepare bytes
        bytes = io.BufferedRandom(io.BytesIO())
        bytes.write(source.encode(encoding))
        bytes.seek(0)

        # Return or raise
        if mode == 'b':
            return (bytes, encoding)
        elif mode == 't':
            chars = io.TextIOWrapper(bytes, self.__encoding)
            return chars
        else:
            message = 'Mode %s is not supported' % mode
            raise RuntimeError(message)
