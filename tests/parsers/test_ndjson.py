# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import io
from mock import Mock
from tabulator import Stream
from tabulator.parsers.ndjson import NDJSONParser


# Tests

def test_ndjson_parser():

    source = 'data/table.ndjson'
    encoding = None
    loader = Mock()
    loader.load = Mock(return_value=io.open(source, encoding='utf-8'))
    parser = NDJSONParser()

    assert parser.closed is True
    parser.open(source, encoding, loader)
    assert parser.closed is False

    assert list(parser.extended_rows) == [
        (1, ['id', 'name'], [1, 'english']),
        (2, ['id', 'name'], [2, '中国人']),
    ]

    assert len(list(parser.extended_rows)) == 0
    parser.reset()
    assert len(list(parser.extended_rows)) == 2

    parser.close()
    assert parser.closed


def test_stream_ndjson():
    with Stream('data/table.ndjson', headers=1) as stream:
        assert stream.headers == ['id', 'name']
        assert stream.read(keyed=True) == [
            {'id': 1, 'name': 'english'},
            {'id': 2, 'name': '中国人'}]
