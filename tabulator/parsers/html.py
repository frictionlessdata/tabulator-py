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
        self.__bytes = None

    @property
    def closed(self):
        return self.__bytes is None or self.__bytes.closed

    def open(self, source, encoding=None):
        self.close()
        self.__encoding = encoding
        self.__bytes = self.__loader.load(source, mode='b', encoding=encoding)
        if self.__encoding:
            self.__encoding.lower()
        self.reset()

    def close(self):
        if not self.closed:
            self.__bytes.close()

    def reset(self):
        helpers.reset_stream(self.__bytes)
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
        page = pq(self.__bytes.read())

        # Find required table
        table = pq(page.find(self.__selector)[0])

        # Extract headers
        rows = (
            table.children('thead').children('tr') +
            table.children('tr') +
            table.children('tbody').children('tr')
        )
        rows = [pq(r) for r in rows]
        first_row = rows.pop(0)
        headers = [pq(th).text() for th in first_row.find('th,td')]

        # Extract rows
        rows = [[pq(td).text()
                 for td in pq(tr).find('td')]
                for tr in rows]

        # Yield rows
        for row_number, row in enumerate(rows, start=1):
            yield (row_number, headers, row)
