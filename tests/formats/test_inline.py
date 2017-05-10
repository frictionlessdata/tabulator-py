# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import pytest
from tabulator import Stream, exceptions


# Stream

def test_stream_inline():
    source = [['id', 'name'], ['1', 'english'], ['2', '中国人']]
    with Stream(source) as stream:
        assert stream.headers is None
        assert stream.read() == [['id', 'name'], ['1', 'english'], ['2', '中国人']]


def test_stream_inline_iterator():
    source = iter([['id', 'name'], ['1', 'english'], ['2', '中国人']])
    with Stream(source) as stream:
        assert stream.headers is None
        assert stream.read() == [['id', 'name'], ['1', 'english'], ['2', '中国人']]


def test_stream_inline_iterator():
    def generator():
        yield ['id', 'name']
        yield ['1', 'english']
        yield ['2', '中国人']
    with pytest.raises(exceptions.SourceError) as excinfo:
        iterator = generator()
        Stream(iterator).open()
    assert 'callable' in str(excinfo.value)


def test_stream_inline_generator():
    def generator():
        yield ['id', 'name']
        yield ['1', 'english']
        yield ['2', '中国人']
    with Stream(generator) as stream:
        assert stream.headers is None
        assert stream.read() == [['id', 'name'], ['1', 'english'], ['2', '中国人']]


def test_stream_inline_keyed():
    source = [{'id': '1', 'name': 'english'}, {'id': '2', 'name': '中国人'}]
    with Stream(source, format='inline') as stream:
        assert stream.headers is None
        assert stream.read() == [['1', 'english'], ['2', '中国人']]
