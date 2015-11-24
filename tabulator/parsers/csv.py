import csv
from io import TextIOWrapper
from .api import API


class CSV(API):

    # Public

    def __init__(self, encoding, **options):
        self.__encoding = encoding
        self.__options = options

    def parse(self, stream):
        # TODO: implement Python2 support
        text_stream = TextIOWrapper(stream, encoding=self.__encoding)
        rows = csv.reader(text_stream, **self.__options)
        for row in rows:
            yield tuple(row)
