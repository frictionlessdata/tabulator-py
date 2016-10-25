# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

from tabulator import Stream


# Tests

def test_stream_csv_options():
    source = 'value1;value2\nvalue3;value4'
    with Stream(source, scheme='text', format='csv', delimiter=';') as stream:
        assert stream.read() == [['value1', 'value2'], ['value3', 'value4']]


def test_stream_json_options():
    source = '{"root": [["value1", "value2"], ["value3", "value4"]]}'
    with Stream(source, scheme='text', format='json', prefix='root') as stream:
        assert stream.read() == [['value1', 'value2'], ['value3', 'value4']]
