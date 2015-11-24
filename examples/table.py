from tabulator import Table, loaders, parsers, processors


table = Table(
        loader=loaders.File('examples/data/valid.csv', encoding='utf-8'),
        parser=parsers.CSV())
table.add_processor(processors.Headers(index=1))
table.open()
headers = table.headers
contents = table.read(with_headers=True, limit=100)
print(headers, contents)
table.close()
