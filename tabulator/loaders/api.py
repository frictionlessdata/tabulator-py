# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

from six import add_metaclass
from abc import ABCMeta, abstractmethod


@add_metaclass(ABCMeta)
class API(object):
    """Loader representation.
    """

    # Public

    @abstractmethod
    def __init__(self, source, encoding=None, **options):
        pass  # pragma: no cover

    @abstractmethod
    def load(self, mode, detect_encoding=True):
        """Load byte/text stream file-like object.
        """
        pass  # pragma: no cover
