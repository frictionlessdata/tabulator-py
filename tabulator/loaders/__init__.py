# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

from .api import Loader as API
from .file import FileLoader as File
from .native import NativeLoader as Native
from .stream import StreamLoader as Stream
from .text import TextLoader as Text
from .web import WebLoader as Web
