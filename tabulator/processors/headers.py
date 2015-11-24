from .api import API


class Headers(API):

    # Public

    def __init__(self, index=1):
        self.__index = index
        self.__headers = None

    def process(self, index, headers, row):
        if self.__headers is not None:
            headers = self.__headers
        if self.__index == index:
            if headers is None:
                self.__headers = row
                # Reset iteration
                index = None
            else:
                # Skip row
                row = None
        return index, headers, row
