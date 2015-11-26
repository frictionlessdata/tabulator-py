from tabulator import topen, loaders, parsers, processors


path = 'https://raw.githubusercontent.com/okfn/tabulator-py/master/examples/data/valid.csv'
with topen(path, encoding='utf-8', format='csv') as table:
    table.add_processor(processors.Headers())
    for row in table.readrow(with_headers=True):
        print(row)


path = 'examples/data/valid.json'
with topen(path, encoding='utf-8', format='json') as table:
    for row in table.readrow(with_headers=True):
        print(row)


path = 'examples/data/valid.xls'
with topen(path, encoding='utf-8', format='excel') as table:
    table.add_processor(processors.Headers())
    for row in table.readrow(with_headers=True):
        print(row)
