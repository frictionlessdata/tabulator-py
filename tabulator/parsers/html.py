# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

from pyquery import PyQuery as pq
from ..parser import Parser
from .. import helpers


# Module API

class HTMLTableParser(Parser):
    """Parser to extract data out of HTML tables
    """

    # Public

    options = [
        'selector',
    ]

    def __init__(self, loader, force_parse=False, selector='table'):
        self.__loader = loader
        self.__selector = selector
        self.__force_parse = force_parse
        self.__extended_rows = None
        self.__encoding = None
        self.__chars = None

    @property
    def closed(self):
        return self.__chars is None or self.__chars.closed

    def open(self, source, encoding=None):
        self.close()
        self.__encoding = encoding
        self.__chars = self.__loader.load(source, encoding=encoding)
        if self.__encoding:
            self.__encoding.lower()
        self.reset()

    def close(self):
        if not self.closed:
            self.__chars.close()

    def reset(self):
        helpers.reset_stream(self.__chars)
        self.__extended_rows = self.__iter_extended_rows()

    @property
    def encoding(self):
        return self.__encoding

    @property
    def extended_rows(self):
        return self.__extended_rows

    # Private

    def __iter_extended_rows(self):

        # Get Page content
        page = pq(self.__chars.read(), parser='html')

        # Find required table
        if self.__selector:
            table = pq(page.find(self.__selector)[0])
        else:
            table = page

        # Extract headers
        rows = (
            table.children('thead').children('tr') +
            table.children('thead') +
            table.children('tr') +
            table.children('tbody').children('tr')
        )
        rows = [pq(r) for r in rows if len(r) > 0]
        first_row = rows.pop(0)
        headers = [pq(th).text() for th in first_row.find('th,td')]

        # Extract rows
        rows = [pq(tr).find('td') for tr in rows]
        rows = [[pq(td).text() for td in tr]
                for tr in rows if len(tr) > 0]

        # Yield rows
        for row_number, row in enumerate(rows, start=1):
            yield (row_number, headers, row)
