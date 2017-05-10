# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

from tabulator import Stream
from tabulator.loaders.local import LocalLoader


# Stream

def test_stream_file():
    with Stream('data/table.csv') as stream:
        assert stream.read() == [['id', 'name'], ['1', 'english'], ['2', '中国人']]


# Loader

def test_loader_local_t():
    loader = LocalLoader()
    chars = loader.load('data/table.csv', encoding='utf-8')
    assert chars.read() == 'id,name\n1,english\n2,中国人\n'


def test_loader_local_b():
    spec = '中国人'.encode('utf-8')
    loader = LocalLoader()
    chars = loader.load('data/table.csv', mode='b', encoding='utf-8')
    assert chars.read() == b'id,name\n1,english\n2,' + spec + b'\n'
