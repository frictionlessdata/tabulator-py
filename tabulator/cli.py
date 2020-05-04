# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
# from __future__ import unicode_literals

import six
import click
import tabulator
from . import config
from . import exceptions


# Module API

@click.command(help='')
@click.argument('source')
@click.option('--headers', type=click.INT)
@click.option('--scheme')
@click.option('--format')
@click.option('--encoding')
@click.option('--limit', type=click.INT)
@click.option('--sheet')
@click.option('--fill_merged_cells', type=click.BOOL)
@click.option('--preserve_formatting', type=click.BOOL)
@click.option('--adjust_floating_point_error', type=click.BOOL)
@click.option('--table')
@click.option('--order_by')
@click.option('--resource')
@click.option('--property')
@click.option('--keyed', type=click.BOOL)
@click.version_option(config.VERSION, message='%(version)s')
def cli(source, limit, **options):
    """Command-line interface

    ```
    Usage: tabulator [OPTIONS] SOURCE

    Options:
      --headers INTEGER
      --scheme TEXT
      --format TEXT
      --encoding TEXT
      --limit INTEGER
      --sheet TEXT/INTEGER (excel)
      --fill_merged_cells BOOLEAN (excel)
      --preserve_formatting BOOLEAN (excel)
      --adjust_floating_point_error BOOLEAN (excel)
      --table TEXT (sql)
      --order_by TEXT (sql)
      --resource TEXT/INTEGER (datapackage)
      --property TEXT (json)
      --keyed BOOLEAN (json)
      --version          Show the version and exit.
      --help             Show this message and exit.
    ```

    """

    # Normalize options
    options = {key: value for key, value in options.items() if value is not None}
    try:
        options['sheet'] = int(options.get('sheet'))
        options['resource'] = int(options.get('resource'))
    except Exception:
        pass

    # Read the table
    try:
        with tabulator.Stream(source, **options) as stream:
            cast = str
            if six.PY2:
                cast = unicode  # noqa
            if stream.headers:
                click.echo(click.style(', '.join(map(cast, stream.headers)), bold=True))
            for count, row in enumerate(stream, start=1):
                click.echo(','.join(map(cast, row)))
                if count == limit:
                    break
    except exceptions.TabulatorException as exception:
        click.echo('[error] %s' % str(exception))
        exit(1)
