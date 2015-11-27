from six import add_metaclass
from abc import ABCMeta, abstractmethod


@add_metaclass(ABCMeta)
class API(object):
    """Loader representation.
    """

    # Public

    @abstractmethod
    def __init__(self, source, encoding=None, **options):
        pass

    @abstractmethod
    def load(self, mode):
        """Return byte stream file-like object.
        """
        pass
