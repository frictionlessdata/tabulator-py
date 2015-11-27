from tabulator import topen, loaders, parsers, processors


with topen('text://id,name\n1,name1\n2,name2\n', format='csv') as table:
    table.add_processor(processors.Headers())
    for row in table.readrow(with_headers=True):
        print(row)


with topen('file://examples/data/table.json') as table:
    for row in table.readrow(with_headers=True):
        print(row)


with topen('examples/data/table.xls') as table:
    table.add_processor(processors.Headers())
    for row in table.readrow(with_headers=True):
        print(row)


source = 'https://raw.githubusercontent.com'
source += '/okfn/tabulator-py/master/examples/data/table.csv'
with topen(source) as table:
    table.add_processor(processors.Headers())
    for row in table.readrow(with_headers=True):
        print(row)
    table.reset()
    print(table.read())
