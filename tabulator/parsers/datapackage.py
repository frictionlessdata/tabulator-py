# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import datapackage
import six

from ..parser import Parser


# Module API

class DataPackageParser(Parser):
    """Parser to extract data from Tabular Data Packages.

    See: http://specs.frictionlessdata.io/
    """

    # Public

    options = [
        'resource',
    ]

    def __init__(self, loader, resource=0):
        self.__resource = resource
        self.__extended_rows = None
        self.__force_parse = None
        self.__datapackage = None
        self.__resource_iter = None

    @property
    def closed(self):
        return self.__resource_iter is None

    def open(self, source, encoding=None, force_parse=False):
        self.close()
        self.__force_parse = force_parse
        self.__datapackage = datapackage.DataPackage(source)
        self.reset()

    def close(self):
        if not self.closed:
            self.__datapackage = None
            self.__resource_iter = None
            self.__extended_rows = None

    def reset(self):
        if isinstance(self.__resource, six.string_types):
            named_resource = next(iter(filter(
                lambda res: res.descriptor['name'] == self.__resource,
                self.__datapackage.resources
            )))  # TODO: use data_package.getResource(name) when v1 is released
            self.__resource_iter = named_resource.iter()
        else:
            self.__resource_iter = \
                self.__datapackage.resources[self.__resource].iter()
        self.__extended_rows = self.__iter_extended_rows()

    @property
    def extended_rows(self):
        return self.__extended_rows

    # Private

    def __iter_extended_rows(self):
        for number, row in enumerate(self.__resource_iter, start=1):
            keys, values = zip(*sorted(row.items()))
            yield number, list(keys), list(values)
