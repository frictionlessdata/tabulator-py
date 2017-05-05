# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

from six import add_metaclass
from abc import ABCMeta, abstractmethod


# Module API

@add_metaclass(ABCMeta)
class Parser(object):

    # Public

    options = []

    def __init__(self, loader, **options):
        """https://github.com/frictionlessdata/tabulator-py#custom-parsers
        """
        pass

    @property
    @abstractmethod
    def closed(self):
        """https://github.com/frictionlessdata/tabulator-py#custom-parsers
        """
        pass  # pragma: no cover

    @abstractmethod
    def open(self, source, encoding=None, force_parse=False):
        """https://github.com/frictionlessdata/tabulator-py#custom-parsers
        """
        pass  # pragma: no cover

    @abstractmethod
    def close(self):
        """https://github.com/frictionlessdata/tabulator-py#custom-parsers
        """
        pass  # pragma: no cover

    @abstractmethod
    def reset(self):
        """https://github.com/frictionlessdata/tabulator-py#custom-parsers
        """
        pass  # pragma: no cover

    @property
    @abstractmethod
    def extended_rows(self):
        """https://github.com/frictionlessdata/tabulator-py#custom-parsers
        """
        pass  # pragma: no cover
