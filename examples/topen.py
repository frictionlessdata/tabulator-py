from tabulator import topen, loaders, parsers, processors


with topen('examples/data/valid.csv', encoding='utf-8', format='csv') as table:
    table.add_processor(processors.Headers(index=1))
    for row in table.readrow(with_headers=True):
        print(row)
