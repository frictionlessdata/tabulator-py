# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import pytest
import sqlite3


# Fixtures

@pytest.fixture
def database_url(tmpdir):
    path = str(tmpdir.join('database.db'))
    conn = sqlite3.connect(path)
    conn.execute('CREATE TABLE data (id INTEGER PRIMARY KEY, name TEXT)')
    conn.execute('INSERT INTO data VALUES (1, "english"), (2, "中国人")')
    conn.commit()
    yield 'sqlite:///%s' % path
    conn.close()
