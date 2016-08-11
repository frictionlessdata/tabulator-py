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

    Args:
        options(dict): loader options

    """

    # Public

    @abstractmethod
    def __init__(self, **options):
        pass  # pragma: no cover

    @abstractmethod
    def load(self, source, encoding, mode):
        """Return byte/text stream file-like object.

        Args:
            source (str): table source
            encoding (str): encoding of source
            mode(str): text stream mode: 't' or 'b'

        Returns:
            file-like: file-like object of byte/text stream

        """
        pass  # pragma: no cover
