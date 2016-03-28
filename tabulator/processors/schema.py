# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

from .. import helpers
from . import api


# Module API

class SchemaProcessor(api.Processor):
    """Processor to add types to row.

    Parameters
    ----------
    schema: str/dict
        Schema as in https://github.com/okfn/jsontableschema-py#model.
        If schema is None processor will cast values using type detection.

    """

    # Public

    def __init__(self, schema=None):
        self.__schema = None
        if schema is not None:
            # TODO: review
            # Import here as a quick fix for:
            # https://github.com/frictionlessdata/tabulator-py/issues/51
            from jsontableschema.model import SchemaModel
            self.__schema = SchemaModel(schema)

    def process(self, iterator):
        if self.__schema is None:
            values = []
            for value in iterator.values:
                value = helpers.parse_value(value)
                values.append(value)
            iterator.values = tuple(values)
        else:
            values = self.__schema.convert_row(*iterator.values)
            iterator.values = tuple(values)

    def handle(self, iterator):
        pass  # pragma: no cover
