import ijson
from .api import API


class JSON(API):
    """Parser to parse JSON data format.
    """

    # Public

    def __init__(self, prefix='item'):
        self.__prefix = prefix
        self.__bytes = None
        self.__items = None

    def open(self, loader):
        self.close()
        self.__loader = loader
        self.__bytes = loader.load(mode='b')
        items = ijson.items(self.__bytes, self.__prefix)
        self.__items = (
            (tuple(item.keys()), tuple(item.values()))
            for item in items)

    def close(self):
        if not self.closed:
            self.__bytes.close()

    @property
    def closed(self):
        return self.__bytes is None or self.__bytes.closed

    @property
    def items(self):
        return self.__items

    def reset(self):
        if not self.__bytes.seekable():
            message = (
                'Loader\'s returned not seekable stream. '
                'For this stream reset is not supported.')
            raise RuntimeError(message)
        return self.__bytes.seek(0)
