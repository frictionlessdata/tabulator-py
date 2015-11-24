from six import add_metaclass
from abc import ABCMeta, abstractmethod


@add_metaclass(ABCMeta)
class API(object):
    """Processor representation.
    """

    # Public

    @abstractmethod
    def process(self, index, headers, row):
        """Return processed (index, headers and row) tuple.
        """
        pass
