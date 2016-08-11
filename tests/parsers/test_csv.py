# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import io
from mock import Mock
from tabulator import parsers


# Tests

def test_csv_parser():

    source = 'data/table.csv'
    encoding = None
    loader = Mock()
    loader.load = Mock(return_value=io.open(source, encoding='utf-8'))
    parser = parsers.CSV()

    assert parser.closed
    parser.open(source, encoding, loader)
    assert not parser.closed

    assert list(parser.items) == [
        (None, ('id', 'name')),
        (None, ('1', 'english')),
        (None, ('2', '中国人'))]

    assert len(list(parser.items)) == 0
    parser.reset()
    assert len(list(parser.items)) == 3

    parser.close()
    assert parser.closed
