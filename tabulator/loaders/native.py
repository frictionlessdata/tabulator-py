# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

from .. import exceptions
from . import api


# Module API

class NativeLoader(api.Loader):
    """Null loader to pass python native lists.
    """

    # Public

    def __init__(self, **options):
        self.__options = options

    def load(self, source, encoding, mode):
        message = 'NativeLoader doesn\'t support load method'
        raise exceptions.LoadingError(message)
