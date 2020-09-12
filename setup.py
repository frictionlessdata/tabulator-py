# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import os
import io
from setuptools import setup, find_packages


# Helpers
def read(*paths):
    """Read a text file."""
    basedir = os.path.dirname(__file__)
    fullpath = os.path.join(basedir, *paths)
    contents = io.open(fullpath, encoding='utf-8').read().strip()
    return contents


# Prepare
PACKAGE = 'tabulator'
INSTALL_REQUIRES = [
    # General
    'six>=1.9',
    'click>=6.0',
    'requests>=2.8',
    'chardet>=3.0',
    'boto3>=1.9',
    # Format: csv
    'unicodecsv>=0.14',
    # Format: json
    'ijson>=3.0.3',
    # Format: ndjson
    'jsonlines>=1.1',
    # Format: sql
    'sqlalchemy>=0.9.6',
    # Format: tsv
    'linear-tsv>=1.0',
    # Format: xls
    'xlrd>=1.0',
    # Format: xlsx
    'openpyxl>=2.6',
]
INSTALL_FORMAT_DATAPACKAGE_REQUIRES = [
    'datapackage>=1.12',
]
INSTALL_FORMAT_ODS_REQUIRES = [
    'ezodf>=0.3',
    'lxml>=3.0',
]
INSTALL_PARSER_HTML_REQUIRES = [
    'pyquery<2',
]
INSTALL_CCHARDET_REQUIRES = [
    'cchardet>=2.0',
]
TESTS_REQUIRE = [
    'mock',
    'pylama',
    'pytest',
    'pytest-cov',
    'moto[server]',
    'tox',
]
README = read('README.md')
VERSION = read(PACKAGE, 'VERSION')
PACKAGES = find_packages(exclude=['examples', 'tests'])


# Run
setup(
    name=PACKAGE,
    version=VERSION,
    packages=PACKAGES,
    include_package_data=True,
    install_requires=INSTALL_REQUIRES,
    tests_require=TESTS_REQUIRE,
    extras_require={
        'datapackage': INSTALL_FORMAT_DATAPACKAGE_REQUIRES,
        'develop': TESTS_REQUIRE,
        'ods': INSTALL_FORMAT_ODS_REQUIRES,
        'html': INSTALL_PARSER_HTML_REQUIRES,
        'cchardet': INSTALL_CCHARDET_REQUIRES,
    },
    entry_points={
        'console_scripts': [
            'tabulator = tabulator.__main__:cli',
        ]
    },
    zip_safe=False,
    long_description=README,
    long_description_content_type='text/markdown',
    description='Consistent interface for stream reading and writing tabular data (csv/xls/json/etc)',
    author='Open Knowledge Foundation',
    author_email='info@okfn.org',
    url='https://github.com/frictionlessdata/tabulator-py',
    license='MIT',
    keywords=[
        'frictionless data',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)
