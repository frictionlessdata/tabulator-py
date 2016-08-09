# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import os
import re
import six
from chardet.universaldetector import UniversalDetector
from six.moves.urllib.parse import urlparse
from . import errors


# Module API

def detect_scheme(source):
    """Detect scheme by source.

    Scheme is a minimum 2 letters before `://` (will be lower cased).
    For example `http` from `http://example.com/table.csv`

    """
    if hasattr(source, 'read'):
        scheme = 'stream'
    elif isinstance(source, six.string_types):
        match = re.search(r'^([a-zA-Z]{2,}):\/{2}', source)
        if not match:
            return None
        scheme = match.group(1).lower()
    else:
        scheme = 'native'
    return scheme


def detect_format(source):
    """Detect format by source.

    For example `csv` from `http://example.com/table.csv`

    """
    if hasattr(source, 'read'):
        format = ''
    elif isinstance(source, six.string_types):
        parsed_source = urlparse(source)
        path = parsed_source.path or parsed_source.netloc
        format = os.path.splitext(path)[1]
        if not format:
            return None
        format = format[1:].lower()
    else:
        format = 'native'
    return format


def detect_encoding(bytes):
    """Detect encoding of a byte stream.
    """
    CHARSET_DETECTION_MAX_LINES = 1000
    CHARSET_DETECTION_MIN_CONFIDENCE = 0.5
    detector = UniversalDetector()
    num_lines = CHARSET_DETECTION_MAX_LINES
    while num_lines > 0:
        line = bytes.readline()
        detector.feed(line)
        if detector.done:
            # TODO: does it work?
            break
        num_lines -= 1
    detector.close()
    bytes.seek(0)
    confidence = detector.result['confidence']
    encoding = detector.result['encoding']
    # Do not use if not confident
    if confidence < CHARSET_DETECTION_MIN_CONFIDENCE:
        encoding = 'utf-8'
    # Default to utf-8 for safety
    if encoding == 'ascii':
        encoding = 'utf-8'
    return encoding


def reset_stream(stream):
    """Reset stream pointer to the first element.

    If stream is not seekable raise Exception.
    """
    try:
        position = stream.tell()
    except Exception:
        position = True
    if position != 0:
        try:
            stream.seek(0)
        except Exception as e:
            print(e)
            message = 'Stream is not seekable.'
            raise errors.Error(message)
