# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import sys

sys.path.insert(0, '.')
from tabulator import topen, loaders, parsers, processors


print('Parse csv format:')
with topen('examples/data/table.csv') as table:
    table.add_processor(processors.Headers())
    print(table.headers)
    for row in table:
        print(row)


print('\nParse json with dicts:')
with topen('file://examples/data/table-dicts.json') as table:
    table.add_processor(processors.Headers())
    print(table.headers)
    for row in table:
        print(row)


print('\nParse json with lists:')
with topen('file://examples/data/table-lists.json') as table:
    table.add_processor(processors.Headers())
    print(table.headers)
    for row in table:
        print(row)


print('\nParse xls format:')
with topen('examples/data/table.xls') as table:
    table.add_processor(processors.Headers())
    print(table.headers)
    for row in table:
        print(row)


print('\nParse xlsx format:')
with topen('examples/data/table.xlsx') as table:
    table.add_processor(processors.Headers())
    print(table.headers)
    for row in table:
        print(row)


print('\nLoad from text scheme:')
with topen('text://id,name\n1,english\n2,中国人\n', format='csv') as table:
    table.add_processor(processors.Headers())
    print(table.headers)
    for row in table:
        print(row)


print('\nLoad from http scheme:')
source = 'https://raw.githubusercontent.com'
source += '/okfn/tabulator-py/master/examples/data/table.csv'
with topen(source) as table:
    table.add_processor(processors.Headers())
    print(table.headers)
    for row in table:
        print(row)


print('\nTable reset and read limit:')
with topen('examples/data/table.csv') as table:
    table.add_processor(processors.Headers())
    print(table.headers)
    print(table.read(limit=1))
    table.reset()
    print(table.read(limit=1))


print('\nLate headers (on a second row):')
with topen('examples/data/special/late_headers.csv') as table:
    table.add_processor(processors.Headers(2))
    print(table.headers)
    for row in table:
        print(row)


print('\nBad headers (skip):')
with topen('examples/data/special/bad_headers.json') as table:
    table.add_processor(processors.Headers())
    table.add_processor(processors.Strict(skip=True))
    print(table.headers)
    for row in table:
        print(row)


print('\nBad headers (raise):')
with topen('examples/data/special/bad_headers.json') as table:
    table.add_processor(processors.Headers())
    table.add_processor(processors.Strict())
    print(table.headers)
    try:
        table.read()
    except Exception as exception:
        print(exception)


print('\nBad dimension (raise):')
with topen('examples/data/special/bad_dimension.csv') as table:
    table.add_processor(processors.Headers())
    table.add_processor(processors.Strict())
    try:
        table.read()
    except Exception as exception:
        print(exception)


print('\nBad headers dimension (raise):')
with topen('examples/data/special/bad_headers_dimension.csv') as table:
    table.add_processor(processors.Headers())
    table.add_processor(processors.Strict())
    try:
        table.read()
    except Exception as exception:
        print(exception)


print('\nUsing schema processor (parse):')
with topen('examples/data/table.csv') as table:
    table.add_processor(processors.Headers())
    table.add_processor(processors.Schema())
    print(table.headers)
    for row in table:
        print(row)


print('\nUsing schema processor (from schema):')
with topen('examples/data/table.csv') as table:
    table.add_processor(processors.Headers())
    table.add_processor(processors.Schema('examples/data/schema.json'))
    print(table.headers)
    for row in table:
        print(row)


print('\nSpaces in headers:')
source = 'https://raw.githubusercontent.com/datasets/gdp/master/data/gdp.csv'
with topen(source) as table:
    table.add_processor(processors.Headers())
    print(table.headers)
    for row in table.read(limit=5):
        print(row)
