from tabulator import topen, loaders, parsers, processors


print('Parse csv format:')
with topen('examples/data/table.csv') as table:
    table.add_processor(processors.Headers())
    for row in table.readrow(with_headers=True):
        print(row)


print('Parse json format:')
with topen('file://examples/data/table.json') as table:
    for row in table.readrow(with_headers=True):
        print(row)


print('Parse xls format:')
with topen('examples/data/table.xls') as table:
    table.add_processor(processors.Headers())
    for row in table.readrow(with_headers=True):
        print(row)


print('Load from text scheme:')
with topen('text://id,name\n1,name1\n2,name2\n', format='csv') as table:
    table.add_processor(processors.Headers())
    for row in table.readrow(with_headers=True):
        print(row)


print('Load from http scheme:')
source = 'https://raw.githubusercontent.com'
source += '/okfn/tabulator-py/master/examples/data/table.csv'
with topen(source) as table:
    table.add_processor(processors.Headers())
    for row in table.readrow(with_headers=True):
        print(row)


print('Table reset and read limit')
with topen('examples/data/table.csv') as table:
    table.add_processor(processors.Headers())
    print(table.read(limit=1))
    table.reset()
    print(table.read(limit=1))
