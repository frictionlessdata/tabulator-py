from .api import API


class Headers(API):

    # Public

    def __init__(self, index=1):
        self.__index = index

    def process(self, index, headers, values):
        if self.__index == index:
            if headers is None:
                # Set headers
                headers = values
                # Reset iteration
                index = None
            # Skip values
            values = None
        return index, headers, values
