# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import io
from mock import Mock
from tabulator import parsers


# Tests

def test_tsv_parser():

    source = 'data/table.tsv'
    encoding = None
    loader = Mock()
    loader.load = Mock(return_value=io.open(source))
    parser = parsers.TSV()

    assert parser.closed
    parser.open(source, encoding, loader)
    assert not parser.closed

    assert list(parser.items) == [
        (None, ('id', 'name')),
        (None, ('1', 'english')),
        (None, ('2', '中国人')),
        (None, ('3', None))]

    assert len(list(parser.items)) == 0
    parser.reset()
    assert len(list(parser.items)) == 4

    parser.close()
    assert parser.closed
