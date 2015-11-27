# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import os
from six.moves.urllib.parse import urlparse


def detect_scheme(source):
    # TODO: rewrite without urlparse
    scheme = urlparse(source).scheme
    return scheme


def detect_format(source):
    format = os.path.splitext(source)[1].replace('.', '')
    return format


def detect_encoding(bytes):
    pass
