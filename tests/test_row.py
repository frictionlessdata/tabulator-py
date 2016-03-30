# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

from tabulator import Row


def test_Row():

    # Initiate
    headers = ['h1', 'h2']
    values = ['v1', 'v2']
    row = Row(headers, values)

    # Assert
    assert row == ('v1', 'v2')
    assert row.get('h1') == 'v1'
    assert row.get('h2') == 'v2'

