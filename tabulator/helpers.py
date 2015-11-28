# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import os
from chardet.universaldetector import UniversalDetector
from six.moves.urllib.parse import urlparse
from . import errors


def detect_scheme(source):
    # TODO: rewrite without urlparse
    scheme = urlparse(source).scheme
    return scheme


def detect_format(source):
    format = os.path.splitext(source)[1].replace('.', '')
    return format


def detect_encoding(bytes):
    detector = UniversalDetector()
    for line in bytes.readlines():
        detector.feed(line)
        if detector.done:
            break
    detector.close()
    bytes.seek(0)
    confidence = detector.result['confidence']
    encoding = detector.result['encoding']
    # Do not use if not confident
    if confidence < 0.95:
        encoding = None
    # Default to utf-8 for safety
    if encoding == 'ascii':
        encoding = 'utf-8'
    return encoding


def reset_stream(stream):
    try:
        position = stream.tell()
    except Exception:
        position = True
    if position != 0:
        if not stream.seekable():
            message = 'Stream is not seekable.'
            raise errors.Error(message)
        stream.seek(0)
