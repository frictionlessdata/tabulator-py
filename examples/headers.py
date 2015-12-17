# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

from tabulator import topen, loaders, parsers, processors


print('Parse csv format:')
with topen('examples/data/table.csv') as table:
    table.add_processor(processors.Headers())
    print(table.headers)
    for row in table.readrow():
        print(row)
