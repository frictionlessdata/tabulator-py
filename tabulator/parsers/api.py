from six import add_metaclass
from abc import ABCMeta, abstractmethod


@add_metaclass(ABCMeta)
class API(object):

    # Public

    @abstractmethod
    def parse(self, stream):
        """Yield one parsed row per step.

        Args:
            stream (file-like): byte stream

        Yields:
            row (tuple): parser row

        """
        pass
