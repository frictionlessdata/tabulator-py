from tabulator import topen, loaders, parsers, processors


print('Parse csv format:')
with topen('examples/data/table.csv') as table:
    table.add_processor(processors.Headers())
    for row in table.readrow(with_headers=True):
        print(row)


print('Parse json with dicts:')
with topen('file://examples/data/table-dicts.json') as table:
    for row in table.readrow(with_headers=True):
        print(row)


print('Parse json with lists:')
with topen('file://examples/data/table-lists.json') as table:
    table.add_processor(processors.Headers())
    for row in table.readrow(with_headers=True):
        print(row)


print('Parse xls format:')
with topen('examples/data/table.xls') as table:
    table.add_processor(processors.Headers())
    for row in table.readrow(with_headers=True):
        print(row)


print('Load from text scheme:')
with topen('text://id,name\n1,english\n2,中国人\n', format='csv') as table:
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


print('Table reset and read limit:')
with topen('examples/data/table.csv') as table:
    table.add_processor(processors.Headers())
    print(table.read(limit=1))
    table.reset()
    print(table.read(limit=1))


print('Late headers (on a second row):')
with topen('examples/data/special/late_headers.csv') as table:
    table.add_processor(processors.Headers(2))
    for row in table.readrow(with_headers=True):
        print(row)


print('Bad headers (skip):')
with topen('examples/data/special/bad_headers.json') as table:
    table.add_processor(processors.Strict(skip=True))
    for row in table.readrow(with_headers=True):
        print(row)


print('Bad headers (raise):')
with topen('examples/data/special/bad_headers.json') as table:
    table.add_processor(processors.Strict())
    try:
        table.read(with_headers=True)
    except Exception as exception:
        print(exception)


print('Bad dimension (raise):')
with topen('examples/data/special/bad_dimension.csv') as table:
    table.add_processor(processors.Headers())
    table.add_processor(processors.Strict())
    try:
        table.read(with_headers=True)
    except Exception as exception:
        print(exception)


print('Bad headers dimension (raise):')
with topen('examples/data/special/bad_headers_dimension.csv') as table:
    table.add_processor(processors.Headers())
    table.add_processor(processors.Strict())
    try:
        table.read(with_headers=True)
    except Exception as exception:
        print(exception)
