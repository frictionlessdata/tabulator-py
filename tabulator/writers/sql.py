# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

from sqlalchemy import create_engine, MetaData, Table, Column, String
from ..writer import Writer
from .. import exceptions


# Module API

class SQLWriter(Writer):
    """SQL writer.
    """

    # Public

    options = [
        'table',
    ]

    def __init__(self, table=None, **options):

        # Ensure table
        if table is None:
            raise exceptions.TabulatorException('Format `sql` requires `table` option.')

        self.__table = table

    def write(self, source, target, headers, encoding=None):
        engine = create_engine(target)
        with engine.begin() as conn:
            meta = MetaData()
            columns = [Column(header, String()) for header in headers]
            table = Table(self.__table, meta, *columns)
            meta.create_all(conn)
            for row in source:
                conn.execute(table.insert(tuple(row)))
