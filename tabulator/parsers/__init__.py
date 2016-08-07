# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

from .api import Parser as API
from .csv import CSVParser as CSV
from .excel import ExcelParser as Excel
from .excelx import ExcelxParser as Excelx
from .json import JSONParser as JSON
from .native import NativeParser as Native
from .tsv import TSVParser as TSV
