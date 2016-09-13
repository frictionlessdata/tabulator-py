# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import io
import sys
from tabulator import Stream


print('Parse csv format:')
source = 'data/table.csv'
with Stream(source, headers='row1') as stream:
    print(stream.headers)
    for row in stream:
        print(row)


print('\nParse linear tsv format:')
source = 'data/table.tsv'
with Stream(source, headers='row1') as stream:
    print(stream.headers)
    for row in stream:
        print(row)


print('\nParse json with dicts:')
source = 'file://data/table-dicts.json'
with Stream(source) as stream:
    print(stream.headers)
    for row in stream:
        print(row)


print('\nParse json with lists:')
source = 'file://data/table-lists.json'
with Stream(source, headers='row1') as stream:
    print(stream.headers)
    for row in stream:
        print(row)


print('\nParse xls format:')
source = 'data/table.xls'
with Stream(source, headers='row1') as stream:
    print(stream.headers)
    for row in stream:
        print(row)


print('\nParse xlsx format:')
source = 'data/table.xlsx'
with Stream(source, headers='row1') as stream:
    print(stream.headers)
    for row in stream:
        print(row)


# print('\nLoad from stream scheme:')
source = io.open('data/table.csv', mode='rb')
with Stream(source, headers='row1', format='csv') as stream:
    print(stream.headers)
    for row in stream:
        print(row)


print('\nLoad from text scheme:')
source = 'text://id,name\n1,english\n2,中国人\n'
with Stream(source, headers='row1', format='csv') as stream:
    print(stream.headers)
    for row in stream:
        print(row)


print('\nLoad from http scheme:')
source = 'https://raw.githubusercontent.com'
source += '/okfn/tabulator-py/master/data/table.csv'
with Stream(source, headers='row1') as stream:
    print(stream.headers)
    for row in stream:
        print(row)


print('\nUsage of native lists:')
source = [['id', 'name'], ['1', 'english'], ('2', '中国人')]
with Stream(source, headers='row1') as stream:
    print(stream.headers)
    for row in stream:
        print(row)


print('\nUsage of native lists (keyed):')
source = [{'id': '1', 'name': 'english'}, {'id': '2', 'name': '中国人'}]
with Stream(source) as stream:
    print(stream.headers)
    for row in stream:
        print(row)


print('\nIter with keyed rows representation:')
source = [{'id': '1', 'name': 'english'}, {'id': '2', 'name': '中国人'}]
with Stream(source, headers=1) as stream:
    print(stream.headers)
    for row in stream.iter(keyed=True):
        print(row)


print('\nTable reset and read limit:')
source = 'data/table.csv'
with Stream(source, headers='row1') as stream:
    print(stream.headers)
    print(stream.read(limit=1))
    stream.reset()
    print(stream.read(limit=1))


print('\nLate headers (on a second row):')
source = 'data/special/late_headers.csv'
with Stream(source, headers='row2') as stream:
    print(stream.headers)
    for row in stream:
        print(row)


print('\nSpaces in headers:')
source = 'https://raw.githubusercontent.com/datasets/gdp/master/data/gdp.csv'
with Stream(source, headers='row1') as stream:
    print(stream.headers)
    for row in stream.read(limit=5):
        print(row)
