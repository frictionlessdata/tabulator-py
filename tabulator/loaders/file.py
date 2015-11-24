import io
from .api import API


class File(API):

    # Public

    def __init__(self, path, encoding):
        self.__path = path
        self.__encoding = encoding

    def load(self):
        return io.open(self.__path, encoding=self.__encoding)
