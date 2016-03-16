# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

from six import add_metaclass
from abc import ABCMeta


# Module API

@add_metaclass(ABCMeta)
class Processor(object):
    """Processor representation.

    Processor will be called on every iteration
    with `process` or `handle` methods. Processor
    can update `Iterator` instance to change
    rows emitted by `Table` instance.

    Parameters
    ----------
    options: dict
        Processing options.

    """

    # Public

    def process(self, iterator):
        """Process iterator in normal mode.

        This method will be called if
        iterator.exception == None.

        Parameters
        ----------
        iterator: `Iterator`
            Table iterator.
        """
        pass  # pragma: no cover

    def handle(self, iterator):
        """Process iterator with exception.

        This method will be called if
        iterator.exception != None.

        Parameters
        ----------
        iterator: `Iterator`
            Table iterator.
        """
        pass  # pragma: no cover
