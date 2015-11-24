from .api import API


class Headers(API):

    # Public

    def __init__(self, index=1):
        self.__index = index

    def process(self, index, headers, row):
        if self.__index == index:
            if headers is None:
                # Set headers
                headers = row
                # Reset iteration
                index = None
            # Skip row
            row = None
        return index, headers, row
