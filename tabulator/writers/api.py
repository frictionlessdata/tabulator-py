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
    """

    # Public

    @abstractmethod
    def write(self, target, encoding, extended_rows, **options):
        """Write tabular data to target.
        """
        pass
