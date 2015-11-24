from six import add_metaclass
from abc import ABCMeta, abstractmethod


@add_metaclass(ABCMeta)
class API(object):

    # Public

    @abstractmethod
    def load(self):
        """Return byte stream file-like object.
        """
        pass
