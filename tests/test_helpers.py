# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import io
import pytest
from tabulator import helpers, config


# Tests

@pytest.mark.parametrize('source, scheme, format', [
    ('text://path', 'text', None),
    ('stream://path', 'stream', None),
    ('file://path', 'file', None),
    ('ftp://path', 'ftp', None),
    ('ftps://path', 'ftps', None),
    ('http://path', 'http', None),
    ('https://path', 'https', None),
    ('xxx://path', 'xxx', None),
    ('xx://path', 'xx', None),
    ('XXX://path', 'xxx', None),
    ('XX://path', 'xx', None),
    ('c://path', 'file', None),
    ('c:\\path', 'file', None),
    (r'c:\path', 'file', None),
    ('http//path', 'file', None),
    ('path', 'file', None),
    ('path.CsV', 'file', 'csv'),
    ('http://someplace.com/foo/path.csv?foo=bar#baz', 'http', 'csv'),
    ('http://someplace.com/foo/path?foo=bar&format=csv#baz', 'http', 'csv'),
    ('https://docs.google.com/spreadsheets/d/X/edit?usp=sharing', None, 'gsheet'),
    ('https://docs.google.com/spreadsheets/d/X/export?format=csv&gid=0&single=true', 'https', 'csv'),
    ('https://docs.google.com/spreadsheets/d/X/pub?gid=0&single=true&output=csv', 'https', 'csv'),
])
def test_detect_scheme_and_format(source, scheme, format):
    assert helpers.detect_scheme_and_format(source) == (scheme, format)


def test_detect_encoding():
    with io.open('Makefile', 'rb') as fp:
        sample = fp.read(config.DEFAULT_BYTES_SAMPLE_SIZE)
        assert helpers.detect_encoding(sample) == 'utf-8'


def test_detect_encoding_windows_1252():
    sample = b'A\n' * 300 + b'\xff\xff'
    try:
        import cchardet
        assert helpers.detect_encoding(sample) == 'cp1252'
    except ImportError:
        assert helpers.detect_encoding(sample) == 'iso8859-1'


def test_detect_encoding_utf_16_be():
    sample = u'\uFEFFthen some text'.encode('utf-16-be')
    assert helpers.detect_encoding(sample) == 'utf-16'


def test_detect_encoding_utf_16_le():
    sample = u'\uFEFFthen some text'.encode('utf-16-le')
    assert helpers.detect_encoding(sample) == 'utf-16'


def test_detect_encoding_unknown():
    sample = b'\xff\x81'
    assert helpers.detect_encoding(sample) == 'utf-8'


def test_reset_stream_seekable():
    file = io.open(__file__)
    file.seek(1)
    assert file.tell() == 1
    helpers.reset_stream(file)
    assert file.tell() == 0


def test_reset_stream_not_seekable():
    with pytest.raises(Exception):
        helpers.reset_stream('not_seekable')


def test_requote_uri():
    url = 'http://next.openspending.org/fdp-adapter/convert?url=https%3A%2F%2Fraw.githubusercontent.com%2Fkravets-levko%2Fdata%2Fmaster%2Ftest.xlsx.csv'
    url1 = 'http://data.defra.gov.uk/ops/government_procurement_card/over_£500_GPC_apr_2013.csv'
    url2 = 'http://data.defra.gov.uk/ops/government_procurement_card/over_%C2%A3500_GPC_apr_2013.csv'
    assert helpers.requote_uri(url) == url
    assert helpers.requote_uri(url1) == url2


def test_import_attribute():
    assert helpers.import_attribute('tabulator.helpers') == helpers


def test_import_attribute_import_error():
    with pytest.raises((ImportError, AttributeError)):
        helpers.import_attribute('tabulator.bad_name')


def test_extract_options():
    names = ['opt1', 'opt2']
    options = {'opt1': 1, 'opt2': 2, 'opt3': 3}
    extracted_options = helpers.extract_options(options, names)
    assert options == {'opt3': 3}
    assert extracted_options == {'opt1': 1, 'opt2': 2}


@pytest.mark.parametrize('sample', [
    ('\n\n\t <html>', True),
    ('<!DOCTYPE html>', True),
    ('col1,col2\nval1,<html>', False),
    ('val1,<html>', False),
])
def test_detect_html(sample):
    text, is_html = sample
    assert helpers.detect_html(text) is is_html


def test_stringify_value():
    sample = '\u4e9c'.encode('utf-8-sig').decode("utf-8")
    assert helpers.stringify_value(sample) == sample


def test_stringify_value_none():
    assert helpers.stringify_value(None) == ''

