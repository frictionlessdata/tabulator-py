# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import os
import io
import json
from setuptools import setup, find_packages


def read(path):
    """Read a text file at the given relative path."""
    basedir = os.path.dirname(__file__)
    return io.open(os.path.join(basedir, path), encoding='utf-8').read()


README = read('README.md')
LICENSE = read('LICENSE.md')
INFO = json.loads(read(os.path.join('tabulator', 'info.json')))
INSTALL_REQUIRES = [
    'six>=1.9',
    'xlrd>=0.9',
    'ijson>=2.0',
    'chardet>=2.0',
    'openpyxl>=2.0',
    'jsontableschema>=0.5'
]
TESTS_REQUIRE = read('tests_require').split()


setup(
    name=INFO['name'],
    version=INFO['version'],
    description=INFO['description'],
    long_description=README,
    author=INFO['author'],
    author_email=INFO['author_email'],
    url=INFO['repository'],
    license=INFO['license'],
    include_package_data=True,
    packages=find_packages(exclude=['examples', 'tests']),
    package_dir={INFO['slug']: INFO['slug']},
    install_requires=INSTALL_REQUIRES,
    tests_require=TESTS_REQUIRE,
    test_suite='make test',
    zip_safe=False,
    keywords=INFO['keywords'],
    classifiers=INFO['classifiers'],
)
