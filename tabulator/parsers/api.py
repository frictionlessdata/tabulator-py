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
    """Parser representation.

    Parameters
    ----------
    options: dict
        Parser options.

    """

    # Public

    @abstractmethod
    def __init__(self, **options):
        pass  # pragma: no cover

    @abstractmethod
    def open(self, loader):
        """Open underlaying stream.

        Parser gets byte or text stream from loader
        to start emit items from this stream.

        Parameters
        ----------
        loader: `Loader`
            Loader instance.

        """
        pass  # pragma: no cover

    @abstractmethod
    def close(self):
        """Close underlaying stream.
        """
        pass  # pragma: no cover

    @property
    @abstractmethod
    def closed(self):
        """Return if underlaynig stream is closed.
        """
        pass  # pragma: no cover

    @property
    @abstractmethod
    def items(self):
        """Items generator.

        Emit from parsed underlaying stream
        keys, values pairs.

        Yields
        ------
        (keys, values): tuple
            Keys, values pairs.

        """
        pass  # pragma: no cover

    @abstractmethod
    def reset(self):
        """Reset items and underlaying stream.

        After reset call iterations over items will
        start from scratch.

        """
        pass  # pragma: no cover
