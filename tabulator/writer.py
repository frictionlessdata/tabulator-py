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
    '''Abstract class implemented by the data writers.

    The writers inherit and implement this class' methods to add support for a
    new file destination.

    Args:
        **options (dict): Writer options.

    Returns:
        Writer: Writer instance.
    '''

    # Public

    options = []

    def __init__(self, **options):
        pass

    @abstractmethod
    def write(self, source, target, headers=None, encoding=None):
        '''Writes source data to target.

        Args:
            source (str): Source data.
            target (str): Write target.
            headers (List[str], optional): List of header names.
            encoding (str, optional): Source file encoding.
        '''
        pass
