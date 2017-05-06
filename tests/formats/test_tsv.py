# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import io
from mock import Mock
from tabulator.parsers.tsv import TSVParser


# Parser

def test_parser_tsv():

    source = 'data/table.tsv'
    encoding = None
    loader = Mock()
    loader.load = Mock(return_value=io.open(source))
    parser = TSVParser(loader)

    assert parser.closed
    parser.open(source, encoding=encoding)
    assert not parser.closed

    assert list(parser.extended_rows) == [
        (1, None, ['id', 'name']),
        (2, None, ['1', 'english']),
        (3, None, ['2', '中国人']),
        (4, None, ['3', None])]

    assert len(list(parser.extended_rows)) == 0
    parser.reset()
    assert len(list(parser.extended_rows)) == 4

    parser.close()
    assert parser.closed
