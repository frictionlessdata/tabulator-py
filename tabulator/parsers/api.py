from six import add_metaclass
from abc import ABCMeta, abstractmethod


@add_metaclass(ABCMeta)
class API(object):
    """Parser representation.
    """

    # Public

    @abstractmethod
    def __init__(self, encoding, **options):
        pass

    @abstractmethod
    def parse(self, stream):
        """Yield one parsed row per step.

        Args:
            stream (file-like): byte stream

        Yields:
            values (tuple): parsed row

        """
        pass
