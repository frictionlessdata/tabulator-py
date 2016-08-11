# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

from tabulator import loaders


# Tests

def test_load_t():
    loader = loaders.File()
    chars = loader.load('data/table.csv', 'utf-8', mode='t')
    assert chars.read() == 'id,name\n1,english\n2,中国人\n'


def test_load_b():
    spec = '中国人'.encode('utf-8')
    loader = loaders.File()
    chars = loader.load('data/table.csv', 'utf-8', mode='b')
    assert chars.read() == b'id,name\n1,english\n2,' + spec + b'\n'
