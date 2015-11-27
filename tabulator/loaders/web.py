import io
from six.moves.urllib.request import urlopen
from .api import API


class Web(API):
    """Loader to load source from the web.
    """

    # Public

    def __init__(self, source, encoding=None, stream=False):
        self.__source = source
        self.__encoding = encoding
        self.__stream = stream

    def load(self, mode):

        # Prepare response
        response = urlopen(self.__source)

        # Prepare encoding
        encoding = response.headers.get_content_charset()
        if self.__encoding is not None:
            encoding = self.__encoding

        # Prepare bytes
        if self.__stream:
            bytes = response
        else:
            bytes = io.BufferedRandom(io.BytesIO())
            bytes.write(response.read())
            bytes.seek(0)

        # Return or raise
        if mode == 'b':
            return (bytes, encoding)
        elif mode == 't':
            chars = io.TextIOWrapper(bytes, encoding)
            return chars
        else:
            message = 'Mode %s is not supported' % mode
            raise RuntimeError(message)
