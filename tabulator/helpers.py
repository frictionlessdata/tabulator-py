# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import codecs
import os
import re
import six
import requests.utils
from bs4 import BeautifulSoup
from six.moves.urllib.parse import urlparse, urlunparse
from chardet.universaldetector import UniversalDetector
from . import exceptions


# Module API

DEFAULT_SCHEME = 'file'
DEFAULT_ENCODING = 'utf-8'
DEFAULT_SAMPLE_SIZE = 100


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


def detect_encoding(bytes, encoding=None):
    """Detect encoding of a byte stream.
    """
    if encoding is not None:
        if encoding.lower() == 'utf-8':
            prefix = bytes.read(len(codecs.BOM_UTF8))
            if prefix == codecs.BOM_UTF8:
                encoding = 'utf-8-sig'
            bytes.seek(0)
        return encoding

    CHARDET_DETECTION_MAX_LINES = 1000
    CHARDET_DETECTION_MIN_CONFIDENCE = 0.5
    detector = UniversalDetector()
    num_lines = CHARDET_DETECTION_MAX_LINES
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
    if confidence < CHARDET_DETECTION_MIN_CONFIDENCE:
        encoding = DEFAULT_ENCODING
    # Default to utf-8 for safety
    if encoding == 'ascii':
        encoding = DEFAULT_ENCODING
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


def ensure_dir(path):
    """Ensure directory exists.

    Args:
        path(str): dir path

    """
    dirpath = os.path.dirname(path)
    if dirpath and not os.path.exists(dirpath):
        os.makedirs(dirpath)


def requote_uri(uri):
    """Requote uri if it contains non-ascii chars, spaces etc.

    Args:
        uri (str): uri to requote

    """
    if six.PY2:
        def url_encode_non_ascii(bytes):
            pattern = '[\x80-\xFF]'
            replace = lambda c: ('%%%02x' % ord(c.group(0))).upper()
            return re.sub(pattern, replace, bytes)
        parts = urlparse(uri)
        uri = urlunparse(
            part.encode('idna') if index == 1
            else url_encode_non_ascii(part.encode('utf-8'))
            for index, part in enumerate(parts))
    return requests.utils.requote_uri(uri)
