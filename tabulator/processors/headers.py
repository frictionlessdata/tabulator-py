from .api import API


class Headers(API):

    # Public

    def __init__(self, index=1):
        self.__index = index

    def process(self, iterator):
        if self.__index == iterator.index:
            if iterator.headers is None:
                # Set headers
                iterator.headers = iterator.values
                # Reset iterator
                if self.__index > 1:
                    iterator.reset()
            # Skip iteration
            iterator.skip()
