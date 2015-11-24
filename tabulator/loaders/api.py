from six import add_metaclass
from abc import ABCMeta, abstractmethod


@add_metaclass(ABCMeta)
class API(object):
    """ Loader representation.
    """

    # Public

    @abstractmethod
    def __init__(self, path, **options):
        pass

    @abstractmethod
    def load(self):
        """Return byte stream file-like object.
        """
        pass
