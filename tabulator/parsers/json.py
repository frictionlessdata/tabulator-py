import ijson
from .api import API


class JSON(API):
    """Parser to parse JSON data format.
    """

    # Public

    def __init__(self, path):
        self.__path = path

    def parse(self, stream):
        items = ijson.items(stream, 'item')
        for item in items:
            keys = tuple(item.keys())
            values = tuple(item.values())
            yield keys, values
