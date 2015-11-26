import ijson
from .api import API


class JSON(API):
    """Parser to parse JSON data format.
    """

    # Public

    def __init__(self, encoding, prefix='item'):
        self.__encoding = encoding
        self.__prefix = prefix
        self.__bytes = None
        self.__items = None

    def open(self, bytes):
        self.__bytes = bytes
        items = ijson.items(bytes, self.__prefix)
        self.__items = (
            (tuple(item.keys()), tuple(item.values()))
            for item in items)

    def close(self):
        self.__bytes.close()

    @property
    def closed(self):
        return self.__bytes is None or self.__bytes.closed

    @property
    def items(self):
        return self.__items

    def reset(self):
        return self.__bytes.seek(0)
