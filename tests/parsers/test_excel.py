# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import io
from mock import Mock
from tabulator import parsers


# Tests

def test_excel_parser():

    source = 'data/table.xls'
    encoding = None
    loader = Mock()
    loader.load = Mock(return_value=io.open(source, 'rb'))
    parser = parsers.Excel()

    assert parser.closed
    parser.open(source, encoding, loader)
    assert not parser.closed

    assert list(parser.extended_rows) == [
        (1, None, ['id', 'name']),
        (2, None, [1.0, 'english']),
        (3, None, [2.0, '中国人'])]

    assert len(list(parser.extended_rows)) == 0
    parser.reset()
    assert len(list(parser.extended_rows)) == 3

    parser.close()
    assert parser.closed
