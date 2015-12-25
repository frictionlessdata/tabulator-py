# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import io
import sys

sys.path.insert(0, '.')
from tabulator import topen, loaders, parsers, processors


print('Parse csv format:')
source = 'examples/data/table.csv'
with topen(source, with_headers=True) as table:
    print(table.headers)
    for row in table:
        print(row)


print('\nParse json with dicts:')
source = 'file://examples/data/table-dicts.json'
with topen(source, with_headers=True) as table:
    print(table.headers)
    for row in table:
        print(row)


print('\nParse json with lists:')
source = 'file://examples/data/table-lists.json'
with topen(source, with_headers=True) as table:
    print(table.headers)
    for row in table:
        print(row)


print('\nParse xls format:')
source = 'examples/data/table.xls'
with topen(source, with_headers=True) as table:
    print(table.headers)
    for row in table:
        print(row)


print('\nParse xlsx format:')
source = 'examples/data/table.xlsx'
with topen(source, with_headers=True) as table:
    print(table.headers)
    for row in table:
        print(row)


print('\nLoad from stream scheme:')
source = io.open('examples/data/table.csv', mode='rb')
with topen(source, with_headers=True, format='csv') as table:
    print(table.headers)
    for row in table:
        print(row)


print('\nLoad from text scheme:')
source = 'text://id,name\n1,english\n2,中国人\n'
with topen(source, with_headers=True, format='csv') as table:
    print(table.headers)
    for row in table:
        print(row)


print('\nLoad from http scheme:')
source = 'https://raw.githubusercontent.com'
source += '/okfn/tabulator-py/master/examples/data/table.csv'
with topen(source, with_headers=True) as table:
    print(table.headers)
    for row in table:
        print(row)


print('\nTable reset and read limit:')
source = 'examples/data/table.csv'
with topen(source, with_headers=True) as table:
    print(table.headers)
    print(table.read(limit=1))
    table.reset()
    print(table.read(limit=1))


print('\nLate headers (on a second row):')
source = 'examples/data/special/late_headers.csv'
with topen(source) as table:
    table.add_processor(processors.Headers(skip=1))
    print(table.headers)
    for row in table:
        print(row)


print('\nBad headers (skip):')
source = 'examples/data/special/bad_headers.json'
with topen(source, with_headers=True) as table:
    table.add_processor(processors.Strict(skip=True))
    print(table.headers)
    for row in table:
        print(row)


print('\nBad headers (raise):')
source = 'examples/data/special/bad_headers.json'
with topen(source, with_headers=True) as table:
    table.add_processor(processors.Strict())
    print(table.headers)
    try:
        table.read()
    except Exception as exception:
        print(exception)


print('\nBad dimension (raise):')
source = 'examples/data/special/bad_dimension.csv'
with topen(source, with_headers=True) as table:
    table.add_processor(processors.Strict())
    try:
        table.read()
    except Exception as exception:
        print(exception)


print('\nBad headers dimension (raise):')
source = 'examples/data/special/bad_headers_dimension.csv'
with topen(source, with_headers=True) as table:
    table.add_processor(processors.Strict())
    try:
        table.read()
    except Exception as exception:
        print(exception)


print('\nUsing schema processor (parse):')
source = 'examples/data/table.csv'
with topen(source, with_headers=True) as table:
    table.add_processor(processors.Schema())
    print(table.headers)
    for row in table:
        print(row)


print('\nUsing schema processor (from schema):')
source = 'examples/data/table.csv'
with topen(source, with_headers=True) as table:
    table.add_processor(processors.Schema('examples/data/schema.json'))
    print(table.headers)
    for row in table:
        print(row)


print('\nSpaces in headers:')
source = 'https://raw.githubusercontent.com/datasets/gdp/master/data/gdp.csv'
with topen(source, with_headers=True) as table:
    print(table.headers)
    for row in table.read(limit=5):
        print(row)
