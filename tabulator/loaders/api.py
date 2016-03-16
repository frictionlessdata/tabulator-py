# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

from six import add_metaclass
from abc import ABCMeta, abstractmethod


# Module API

@add_metaclass(ABCMeta)
class Loader(object):
    """Loader representation.

    Parameters
    ----------
    source: str
        Table source.
    encoding: str
        Table encoding.
    options: dict
        Loader options.

    """

    # Public

    @abstractmethod
    def __init__(self, source, encoding=None, **options):
        pass  # pragma: no cover

    @abstractmethod
    def load(self, mode):
        """Return byte/text stream file-like object.

        Parameters
        ----------
        mode: str
            Text stream mode: 't' or 'b'.

        Returns
        -------
        file-like
            File-like object of byte/text stream.

        """
        pass  # pragma: no cover

    @property
    def encoding(self):
        """User defined encoding.

        This property returns encoding set by user
        on Loader creation. No detection here.

        """
        pass  # pragma: no cover
