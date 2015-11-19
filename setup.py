from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import os
import io
import json
from setuptools import setup, find_packages


# Prepare
basedir = os.path.dirname(__file__)
package = json.load(open(os.path.join(basedir, 'package.json')))
readme = open(os.path.join(basedir, 'README.md')).read()
license = open(os.path.join(basedir, 'LICENSE.txt')).read()
requirements = open(os.path.join(basedir, 'requirements.txt')).read().split()
requirements_dev = open(os.path.join(basedir, 'requirements.dev.txt')).read().split()

# Run
setup(
    name=package['name'],
    version=package['version'],
    description=package['description'],
    long_description=readme,
    author=package['author'],
    author_email=package['author_email'],
    url=package['repository'],
    license=package['license'],
    include_package_data=True,
    packages=find_packages(exclude=['demo', 'tests']),
    package_data={'': [readme, license]},
    package_dir={package['slug']: package['slug']},
    include_package_data=True,
    install_requires=requirements,
    tests_require=requirements_dev,
    test_suite='nose.collector',
    zip_safe=False,
    keywords=package['keywords'],
    classifiers=package['classifiers'],
)
