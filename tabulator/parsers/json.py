import ijson
from .api import API


class JSON(API):
    """Parser to parse JSON data format.
    """

    # Public

    def __init__(self, path):
        self.__path = path

    def parse(self, stream):
        rows = ijson.items(stream, 'item')
        for row in rows:
            yield row
