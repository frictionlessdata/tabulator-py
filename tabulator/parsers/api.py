# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

from six import add_metaclass
from abc import ABCMeta, abstractmethod


@add_metaclass(ABCMeta)
class API(object):
    """Parser representation.
    """

    # Public

    @abstractmethod
    def __init__(self, **options):
        pass  # pragma: no cover

    @abstractmethod
    def open(self, loader):
        pass  # pragma: no cover

    @abstractmethod
    def close(self):
        pass  # pragma: no cover

    @property
    @abstractmethod
    def closed(self):
        pass  # pragma: no cover

    @property
    @abstractmethod
    def items(self):
        pass  # pragma: no cover

    @abstractmethod
    def reset(self):
        pass  # pragma: no cover
