from six import add_metaclass
from abc import ABCMeta, abstractmethod


@add_metaclass(ABCMeta)
class API(object):
    """Processor representation.
    """

    @abstractmethod
    def __init__(self, **option):
        pass

    # Public

    @abstractmethod
    def process(self, iterator):
        """Process iterator in normal mode.
        """
        pass

    @abstractmethod
    def handle(self, iterator):
        """Process iterator with exception.
        """
        pass
