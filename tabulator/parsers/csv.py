import csv
from .api import API


class CSV(API):

    # Public

    def __init__(self, **options):
        self.__options = options

    def parse(self, stream):
        rows = csv.reader(stream, **self.__options)
        for row in rows:
            yield tuple(row)
