# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import re
import ast
from chardet.universaldetector import UniversalDetector
from six.moves.urllib.parse import urlparse

from . import errors


# Module API

def detect_scheme(source):
    """Detect scheme by source.

    Schema is a minimum 2 letters before `://` (will be lower cased).
    For example `http` from `http://example.com/table.csv`

    """
    if hasattr(source, 'read'):
        scheme = 'stream'
    else:
        match = re.search(r'^([a-zA-Z]{2,}):\/{2}', source)
        if not match:
            return None
        scheme = match.group(1).lower()
    return scheme


def detect_format(source):
    """Detect format by source.

    For example `csv` from `http://example.com/table.csv`

    """
    if hasattr(source, 'read'):
        format = ''
    else:
        parsed_source = urlparse(source)
        path = parsed_source.path
        if not path:
            # FIXME: This supports valid paths like file://foo.csv, but also
            # invalid ones like http://foo.csv
            path = parsed_source.netloc
        format = path.split('.')[-1].lower()
    return format


def detect_encoding(bytes):
    """Detect encoding of a byte stream.
    """
    detector = UniversalDetector()
    for line in bytes.readlines():
        detector.feed(line)
        if detector.done:
            # TODO: does it work?
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


def parse_value(value):
    """Parse value as a literal.
    """
    try:
        if isinstance(value, str):
            value = ast.literal_eval(value)
    except Exception:
        pass
    return value
