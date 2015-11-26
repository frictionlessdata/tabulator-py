from .api import API


class Headers(API):

    # Public

    def __init__(self, input_index=1):
        self.__input_index = input_index

    def process(self, iterator):
        if self.__input_index == iterator.input_index:
            if iterator.headers is None:
                # Set headers
                iterator.headers = iterator.values
                # Reset iterator
                if self.__input_index > 1:
                    iterator.reset()
            # Skip iteration
            iterator.skip()
