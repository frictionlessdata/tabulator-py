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
    '''Abstract class implemented by the data loaders

    The loaders inherit and implement this class' methods to add support for a
    new scheme (e.g. ssh).

    Args:
        bytes_sample_size (int): Sample size in bytes
        **options (dict): Loader options

    Returns:
        Loader: Loader instance.
    '''

    # Public

    options = []

    def __init__(self, bytes_sample_size, **options):
        pass

    @abstractmethod
    def load(self, source, mode='t', encoding=None):
        '''Load source file.

        Args:
            source (str): Path to tabular source file.
            mode (str, optional): Text stream mode, `t` (text) or `b` (binary).
                Defaults to `t`.
            encoding (str, optional): Source encoding. Auto-detect by default.

        Returns:
            Union[TextIO, BinaryIO]: I/O stream opened either as text or binary.
        '''
        pass
