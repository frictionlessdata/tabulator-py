# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import io
import sys
from tabulator import topen, loaders, parsers


print('Parse csv format:')
source = 'data/table.csv'
with topen(source, headers='row1') as table:
    print(table.headers)
    for row in table:
        print(row)


print('\nParse linear tsv format:')
source = 'data/table.tsv'
with topen(source, headers='row1') as table:
    print(table.headers)
    for row in table:
        print(row)


print('\nParse json with dicts:')
source = 'file://data/table-dicts.json'
with topen(source) as table:
    print(table.headers)
    for row in table:
        print(row)


print('\nParse json with lists:')
source = 'file://data/table-lists.json'
with topen(source, headers='row1') as table:
    print(table.headers)
    for row in table:
        print(row)


print('\nParse xls format:')
source = 'data/table.xls'
with topen(source, headers='row1') as table:
    print(table.headers)
    for row in table:
        print(row)


print('\nParse xlsx format:')
source = 'data/table.xlsx'
with topen(source, headers='row1') as table:
    print(table.headers)
    for row in table:
        print(row)


# print('\nLoad from stream scheme:')
source = io.open('data/table.csv', mode='rb')
with topen(source, headers='row1', format='csv') as table:
    print(table.headers)
    for row in table:
        print(row)


print('\nLoad from text scheme:')
source = 'text://id,name\n1,english\n2,中国人\n'
with topen(source, headers='row1', format='csv') as table:
    print(table.headers)
    for row in table:
        print(row)


print('\nLoad from http scheme:')
source = 'https://raw.githubusercontent.com'
source += '/okfn/tabulator-py/master/data/table.csv'
with topen(source, headers='row1') as table:
    print(table.headers)
    for row in table:
        print(row)


print('\nUsage of native lists:')
source = [['id', 'name'], ['1', 'english'], ('2', '中国人')]
with topen(source, headers='row1') as table:
    print(table.headers)
    for row in table:
        print(row)


print('\nUsage of native lists (keyed):')
source = [{'id': '1', 'name': 'english'}, {'id': '2', 'name': '中国人'}]
with topen(source) as table:
    print(table.headers)
    for row in table:
        print(row)


print('\nIter with keyed rows representation:')
source = [{'id': '1', 'name': 'english'}, {'id': '2', 'name': '中国人'}]
with topen(source) as table:
    print(table.headers)
    for row in table.iter(keyed=True):
        print(row)


print('\nTable reset and read limit:')
source = 'data/table.csv'
with topen(source, headers='row1') as table:
    print(table.headers)
    print(table.read(limit=1))
    table.reset()
    print(table.read(limit=1))


print('\nLate headers (on a second row):')
source = 'data/special/late_headers.csv'
with topen(source, headers='row2') as table:
    print(table.headers)
    for row in table:
        print(row)


print('\nSpaces in headers:')
source = 'https://raw.githubusercontent.com/datasets/gdp/master/data/gdp.csv'
with topen(source, headers='row1') as table:
    print(table.headers)
    for row in table.read(limit=5):
        print(row)
