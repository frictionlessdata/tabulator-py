# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
# from __future__ import unicode_literals

from click.testing import CliRunner
from tabulator.cli import cli


# Tests

def test_cli():
    runner = CliRunner()
    result = runner.invoke(cli, ['data/table.csv'])
    assert result.exit_code == 0
    assert result.output.startswith('id,name\n1,english\n2,')


def test_cli_version():
    runner = CliRunner()
    result = runner.invoke(cli, ['--version'])
    assert result.exit_code == 0
    assert len(result.output.split('.')) == 3
