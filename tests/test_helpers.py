# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import io
import pytest
from tabulator import helpers


# Tests

def test_detect_scheme():
    assert helpers.detect_scheme('text://path') == 'text'
    assert helpers.detect_scheme('stream://path') == 'stream'
    assert helpers.detect_scheme('file://path') == 'file'
    assert helpers.detect_scheme('ftp://path') == 'ftp'
    assert helpers.detect_scheme('ftps://path') == 'ftps'
    assert helpers.detect_scheme('http://path') == 'http'
    assert helpers.detect_scheme('https://path') == 'https'
    assert helpers.detect_scheme('xxx://path') == 'xxx'
    assert helpers.detect_scheme('xx://path') == 'xx'
    assert helpers.detect_scheme('XXX://path') == 'xxx'
    assert helpers.detect_scheme('XX://path') == 'xx'
    assert helpers.detect_scheme('c://path') == None
    assert helpers.detect_scheme('c:\\path') == None
    assert helpers.detect_scheme('c:\path') == None
    assert helpers.detect_scheme('http:/path') == None
    assert helpers.detect_scheme('http//path') == None
    assert helpers.detect_scheme('path') == None


def test_detect_format():
    assert helpers.detect_format('path.CsV') == 'csv'


def test_detect_format_works_with_urls_with_query_and_fragment_components():
    url = 'http://someplace.com/foo/path.csv?foo=bar#baz'
    assert helpers.detect_format(url) == 'csv'


def test_detect_encoding():
    bytes = io.open('README.md', 'rb')
    assert helpers.detect_encoding(bytes) == 'utf-8'


def test_detect_encoding_unknown():
    bytes = io.BytesIO(b'\xff\x81')
    assert helpers.detect_encoding(bytes) == 'utf-8'


def test_detect_encoding_long():
    bytes = io.BytesIO(b'A\n' * 1000 + b'\xff\xff')
    assert helpers.detect_encoding(bytes) == 'utf-8'


def test_detect_encoding_not_so_long():
    bytes = io.BytesIO(b'A\n' * 999 + b'\xff\xff')
    assert helpers.detect_encoding(bytes) == 'windows-1252'


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
