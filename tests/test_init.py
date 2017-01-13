# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import tabulator


# Tests

def test_public_api():
    assert isinstance(tabulator.Stream, type)
    assert isinstance(tabulator.exceptions, object)
    assert len(tabulator.__version__.split('.')) == 3
