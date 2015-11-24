import io
from .api import API


class File(API):
    """Loader to load source from filesystem.
    """

    # Public

    def __init__(self, path):
        self.__path = path

    def load(self):
        return io.open(self.__path, 'rb')
