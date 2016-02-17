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
def read(*paths):
    """Read a text file."""
    basedir = os.path.dirname(__file__)
    fullpath = os.path.join(basedir, *paths)
    contents = io.open(fullpath, encoding='utf-8').read().strip()
    return contents


# Prepare
NAME = 'tabulator'
INSTALL_REQUIRES = [
    'six>=1.9',
    'xlrd>=0.9',
    'ijson>=2.0',
    'chardet>=2.0',
    'openpyxl>=2.0',
    'jsontableschema>=0.5',
]
TESTS_REQUIRE = [
    'tox',
]
VERSION = read(NAME, 'VERSION')
PACKAGES = find_packages(exclude=['examples', 'tests'])
LONG_DESCRIPTION = read('README.md')


# Run
setup(
    name=NAME,
    version=VERSION,
    packages=PACKAGES,
    include_package_data=True,
    install_requires=INSTALL_REQUIRES,
    tests_require=TESTS_REQUIRE,
    extras_require = {'develop': TESTS_REQUIRE},
    test_suite='tox',
    zip_safe=False,
    long_description=LONG_DESCRIPTION,
    description='A utility library that provides a consistent interface for reading tabular data.',
    author='Open Knowledge Foundation',
    author_email='info@okfn.org',
    url='https://github.com/okfn/tabulator-py',
    license='MIT',
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
