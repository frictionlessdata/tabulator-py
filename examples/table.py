from tabulator import Table, loaders, parsers, processors


table = Table(
        loader=loaders.File('examples/data/valid.csv', encoding='utf-8'),
        parser=parsers.CSV())
table.add_processor(processors.Headers())
table.open()
headers = table.headers
contents = table.read(with_headers=True, limit=100)
print(headers, contents)
table.close()


table = Table(
        loader=loaders.Text('id,name\n1,Joe\n2,Rachel\n'),
        parser=parsers.CSV())
with table.open() as table:
    table.add_processor(processors.Headers())
    for row in table.readrow(with_headers=True):
        print(row)
