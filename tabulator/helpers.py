# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import os
import re
import six
import codecs
from copy import copy
from importlib import import_module
from six.moves.urllib.parse import urlparse, urlunparse
from . import exceptions
from . import config


# Module API

def detect_scheme_and_format(source):
    """Detect scheme and format based on source and return as a tuple.

    Scheme is a minimum 2 letters before `://` (will be lower cased).
    For example `http` from `http://example.com/table.csv`

    """

    # Scheme: stream
    if hasattr(source, 'read'):
        return ('stream', None)

    # Format: inline
    if not isinstance(source, six.string_types):
        return (None, 'inline')

    # Format: gsheet
    if 'docs.google.com/spreadsheets' in source:
        if 'export' not in source:
            return (None, 'gsheet')

    # Format: sql
    for sql_scheme in config.SQL_SCHEMES:
        if source.startswith('%s://' % sql_scheme):
            return (None, 'sql')

    # General
    parsed = urlparse(source)
    scheme = parsed.scheme.lower()
    if len(scheme) < 2:
        scheme = config.DEFAULT_SCHEME
    format = os.path.splitext(parsed.path or parsed.netloc)[1][1:].lower() or None

    # Format: datapackage
    if parsed.path.endswith('datapackage.json'):
        return (None, 'datapackage')

    return (scheme, format)


def detect_encoding(sample, encoding=None):
    """Detect encoding of a byte string sample.
    """
    # To reduce tabulator import time
    from cchardet import detect
    def detect_utf8_sig(sample, encoding):
        if encoding == 'utf-8':
            if sample.startswith(codecs.BOM_UTF8):
                encoding = 'utf-8-sig'
        return encoding
    if encoding is not None:
        encoding = encoding.lower()
        return detect_utf8_sig(sample, encoding)
    result = detect(sample)
    confidence = result['confidence'] or 0
    encoding = (result['encoding'] or '').lower()
    encoding = detect_utf8_sig(sample, encoding)
    if confidence < config.ENCODING_CONFIDENCE:
        encoding = config.DEFAULT_ENCODING
    if encoding == 'ascii':
        encoding = config.DEFAULT_ENCODING
    return encoding


def detect_zip(sample):
    """Detect if byte string sample is ZIP.
    """
    SIGNATURE = b'\x50\x4b\x03\x04'
    return sample.startswith(SIGNATURE)


def detect_html(text):
    """Detect if text is HTML.
    """
    pattern = re.compile('\s*<(!doctype|html)', re.IGNORECASE)
    return bool(pattern.match(text))


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
            raise exceptions.ResetError(message)


def ensure_dir(path):
    """Ensure path directory exists.
    """
    dirpath = os.path.dirname(path)
    if dirpath and not os.path.exists(dirpath):
        os.makedirs(dirpath)


def requote_uri(uri):
    """Requote uri if it contains non-ascii chars, spaces etc.
    """
    # To reduce tabulator import time
    import requests.utils
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


def import_attribute(path):
    """Import attribute by path like `package.module.attribute`
    """
    module_name, attribute_name = path.rsplit('.', 1)
    module = import_module(module_name)
    attribute = getattr(module, attribute_name)
    return attribute


def extract_options(options, names):
    """Return options for names and remove it from given options in-place.
    """
    result = {}
    for name, value in copy(options).items():
        if name in names:
            result[name] = value
            del options[name]
    return result


def stringify_value(value):
    """Convert any value to string.
    """
    isoformat = getattr(value, 'isoformat', None)
    if isoformat is not None:
        value = isoformat()
    return str(value)
