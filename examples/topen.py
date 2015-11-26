from tabulator import topen, loaders, parsers, processors


source = b'id,name\n1,Joe\n2,Rachel\n'
with topen(source, encoding='utf-8', format='csv') as table:
    table.add_processor(processors.Headers())
    for row in table.readrow(with_headers=True):
        print(row)
    table.reset()
    print(table.read())


path = 'https://raw.githubusercontent.com/okfn/tabulator-py/master/examples/data/valid.csv'
with topen(path, encoding='utf-8', format='csv') as table:
    table.add_processor(processors.Headers())
    for row in table.readrow(with_headers=True):
        print(row)
    table.reset()
    print(table.read())


path = 'examples/data/valid.json'
with topen(path, encoding='utf-8', format='json') as table:
    for row in table.readrow(with_headers=True):
        print(row)


path = 'examples/data/valid.xls'
with topen(path, encoding='utf-8', format='excel') as table:
    table.add_processor(processors.Headers())
    for row in table.readrow(with_headers=True):
        print(row)
