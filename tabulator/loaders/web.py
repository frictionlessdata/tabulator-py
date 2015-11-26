import io
from six.moves.urllib.request import urlopen
from .api import API


class Web(API):
    """Loader to load source from the web.
    """

    # Public

    def __init__(self, path, stream=False):
        self.__path = path
        self.__stream = stream

    def load(self):
        document = urlopen(self.__path)
        if self.__stream:
            return document
        else:
            stream = io.BufferedRandom(io.BytesIO())
            stream.write(document.read())
            stream.seek(0)
            return stream
