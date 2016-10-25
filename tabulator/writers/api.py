# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

from six import add_metaclass
from abc import ABCMeta, abstractmethod


# Module API

@add_metaclass(ABCMeta)
class Writer(object):
    """Writer representation.

    Args:
        options(dict): writer options

    """

    # Public

    @property
    # @abstractmethod
    def options(self):
        """list: list of available options
        """
        pass

    @abstractmethod
    def write(self, target, encoding, extended_rows):
        """Write tabular data to target.
        """
        pass
