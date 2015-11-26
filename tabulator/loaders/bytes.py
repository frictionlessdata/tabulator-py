import io
from .api import API


class Bytes(API):
    """Loader to load source from bytes.
    """

    # Public

    def __init__(self, source):
        self.__source = source

    def load(self):
        stream = io.BufferedRandom(io.BytesIO())
        stream.write(self.__source)
        stream.seek(0)
        return stream
