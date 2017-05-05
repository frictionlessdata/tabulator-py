# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

from tabulator.loaders.remote import RemoteLoader
SOURCE = 'https://raw.githubusercontent.com/frictionlessdata/tabulator-py/master/data/table.csv'


# Tests

def test_load_t():
    loader = RemoteLoader()
    chars = loader.load(SOURCE, encoding='utf-8')
    assert chars.read() == 'id,name\n1,english\n2,中国人\n'


def test_load_b():
    spec = '中国人'.encode('utf-8')
    loader = RemoteLoader()
    chars = loader.load(SOURCE, mode='b', encoding='utf-8')
    assert chars.read() == b'id,name\n1,english\n2,' + spec + b'\n'