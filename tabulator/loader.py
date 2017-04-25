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

    # Public

    options = []

    def __init__(self, **options):
        """https://github.com/frictionlessdata/tabulator-py#custom-loaders
        """
        pass

    @abstractmethod
    def load(self, source, mode='t', encoding=None, allow_zip=False):
        """https://github.com/frictionlessdata/tabulator-py#custom-loaders
        """
        pass
