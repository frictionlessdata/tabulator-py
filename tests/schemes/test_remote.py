# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import pytest
from tabulator import Stream
from tabulator.loaders.remote import RemoteLoader
BASE_URL = 'https://raw.githubusercontent.com/okfn/tabulator-py/master/%s'


# Stream

def test_stream_https():
    with Stream(BASE_URL % 'data/table.csv') as stream:
        assert stream.read() == [['id', 'name'], ['1', 'english'], ['2', '中国人']]


def test_stream_https_latin1():
    # Github returns wrong encoding `utf-8`
    with Stream(BASE_URL % 'data/special/latin1.csv') as stream:
        assert stream.read()


# Loader

def test_loader_remote_t():
    loader = RemoteLoader()
    chars = loader.load(BASE_URL % 'data/table.csv', encoding='utf-8')
    assert chars.read() == 'id,name\n1,english\n2,中国人\n'


def test_loader_remote_b():
    spec = '中国人'.encode('utf-8')
    loader = RemoteLoader()
    chars = loader.load(BASE_URL % 'data/table.csv', mode='b', encoding='utf-8')
    assert chars.read() == b'id,name\n1,english\n2,' + spec + b'\n'
