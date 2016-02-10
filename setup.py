# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import os
import io
import json
from setuptools import setup, find_packages


# Helpers
def read(path):
    basedir = os.path.dirname(__file__)
    return io.open(os.path.join(basedir, path), encoding='utf-8').read()
def version(package):
    return '0.3.2' # implement parsing


# Prepare
NAME = 'tabulator'
INSTALL_REQUIRES = [
    'six',
    'xlrd',
    'ijson',
    'chardet',
    'openpyxl',
    'jsontableschema',
]
TESTS_REQUIRE = [
    'pylint',
    'tox',
    'mock',
    'pytest',
    'pytest-cov',
    'coverage',
    'coveralls',
]
README = read('README.md')
LICENSE = read('LICENSE.md')
VERSION = version(NAME)
PACKAGES = find_packages(exclude=['examples', 'tests'])


# Run
setup(
    name='tabulator',
    version=VERSION,
    packages=PACKAGES,
    include_package_data=True,
    install_requires=INSTALL_REQUIRES,
    tests_require=TESTS_REQUIRE,
    extras_require = {'development': TESTS_REQUIRE},
    test_suite='make test',
    zip_safe=False,
    description='A utility library that provides a consistent interface for reading tabular data.',
    author='Open Knowledge Foundation',
    author_email='info@okfn.org',
    url='https://github.com/okfn/tabulator-py',
    license=LICENSE,
    keywords="frictionless data",
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
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)
