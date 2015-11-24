from six.moves.urllib.request import urlopen
from .api import API


class Web(API):
    """Loader to load source from the web.
    """

    # Public

    def __init__(self, path):
        self.__path = path

    def load(self):
        return urlopen(self.__path)
