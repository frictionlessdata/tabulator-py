import csv
from codecs import iterdecode
from .api import API


class CSV(API):
    """Parser to parse CSV data format.
    """

    # Public

    def __init__(self, encoding, strategy='replace', **options):
        self.__encoding = encoding
        self.__strategy = strategy
        self.__options = options

    def parse(self, stream):
        # TODO: implement Python2 support
        text_stream = iterdecode(stream, self.__encoding, self.__strategy)
        items = csv.reader(text_stream, **self.__options)
        for item in items:
            keys = None
            values = tuple(item)
            yield keys, values
