# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

from .. import errors
from . import api


# Module API

class NativeLoader(api.Loader):
    """Null loader to pass python native lists.
    """

    # Public

    def __init__(self, source, encoding=None, **options):
        self.__source = source
        self.__encoding = encoding
        self.__options = options

    def load(self, mode):
        raise errors.Error('NativeLoader doesn\'t support load method')

    @property
    def source(self):
        return self.__source

    @property
    def encoding(self):
        return self.__encoding
