# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import io
from mock import Mock
from tabulator import parsers


# Tests

def test_excelx_parser():

    source = 'data/table.xlsx'
    encoding = None
    loader = Mock()
    loader.load = Mock(return_value=io.open(source, 'rb'))
    parser = parsers.Excelx()

    assert parser.closed
    parser.open(source, encoding, loader)
    assert not parser.closed

    assert list(parser.items) == [
        (None, ('id', 'name')),
        (None, (1.0, 'english')),
        (None, (2.0, '中国人'))]

    assert len(list(parser.items)) == 0
    parser.reset()
    assert len(list(parser.items)) == 3

    parser.close()
    assert parser.closed
