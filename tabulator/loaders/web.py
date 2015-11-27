import io
from six.moves.urllib.request import urlopen
from .api import API


class Web(API):
    """Loader to load source from the web.
    """

    # Public

    def __init__(self, source, encoding, stream=False):
        self.__source = source
        self.__encoding = encoding
        self.__stream = stream

    def load(self, mode):
        document = urlopen(self.__source)
        if self.__stream:
            bytes = document
        else:
            bytes = io.BufferedRandom(io.BytesIO())
            bytes.write(document.read())
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
