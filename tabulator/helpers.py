# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import os
import re
import ast
import six
from bs4 import BeautifulSoup
from functools import partial
from six.moves.urllib.parse import urlparse
from chardet.universaldetector import UniversalDetector
from . import exceptions


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


def detect_html(text):
    """Detect if text is HTML.
    """
    return bool(BeautifulSoup(text, 'html.parser').find())


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
        except Exception:
            message = 'Stream is not seekable.'
            raise exceptions.LoadingError(message)


def convert_row(row):
    """Convert row values to python objects.
    """
    result = []
    for value in row:
        try:
            if isinstance(value, six.string_types):
                value = ast.literal_eval(value)
        except Exception:
            pass
        result.append(value)
    return result


def bindify(function):
    """Add bind method to function.
    """
    function.bind = partial(partial, function)
    return function
