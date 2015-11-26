from six import add_metaclass
from abc import ABCMeta, abstractmethod


@add_metaclass(ABCMeta)
class API(object):
    """Parser representation.
    """

    # Public

    @abstractmethod
    def __init__(self, encoding):
        pass

    @abstractmethod
    def open(self):
        pass

    @abstractmethod
    def close(self):
        pass

    @property
    @abstractmethod
    def closed(self):
        pass

    @property
    @abstractmethod
    def items(self):
        pass

    @abstractmethod
    def reset(self):
        pass
