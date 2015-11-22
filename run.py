# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import io
import os
import json
import argparse
import subprocess


# Helpers
def read(path):
    basedir = os.path.dirname(__file__)
    return io.open(os.path.join(basedir, path), encoding='utf-8').read()


# Prepare
package = json.loads(read('package.json'))


# Run
parser = argparse.ArgumentParser(description='Project interface for devs.')
parser.add_argument('script', help='script name to execute')
args = parser.parse_args()
script = package['scripts'][args.script]
print('+ %s' % script)
exit(subprocess.call(script, shell=True))
