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
        self.__bytes = None
        self.__items = None

    def open(self, bytes):
        # TODO: implement Python2 support
        self.close()
        self.__bytes = bytes
        chars = iterdecode(bytes, self.__encoding, self.__strategy)
        items = csv.reader(chars, **self.__options)
        self.__items = ((None, tuple(line)) for line in items)

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
                'Loader\'s returned not seekable byte stream. '
                'For this kind of stream reset is not supported.')
            raise RuntimeError(message)
        return self.__bytes.seek(0)
