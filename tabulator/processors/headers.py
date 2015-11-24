from .api import API


class Headers(API):

    # Public

    def __init__(self, index=1):
        self.__index = index
        self.__headers = None

    def process(self, index, headers, row):
        headers = self.__headers or headers
        if self.__index == index:
            if headers is None:
                self.__headers = row
                # Reset iteration
                index = None
                # Skip row
                row = None
            else:
                # Skip row
                row = None
        return index, headers, row
