# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
# from __future__ import unicode_literals

import six
import click
from .stream import Stream


# Module API

@click.command()
@click.argument('source')
@click.option('--headers', type=click.INT)
@click.option('--scheme')
@click.option('--format')
@click.option('--encoding')
@click.option('--limit', type=click.INT)
def cli(source, limit, **options):
    options = {key: value for key, value in options.items() if value is not None}
    with Stream(source, **options) as stream:
        cast = str
        if six.PY2:
            cast = unicode  # noqa
        if stream.headers:
            click.echo(click.style(', '.join(map(cast, stream.headers)), bold=True))
        for count, row in enumerate(stream, start=1):
            click.echo(', '.join(map(cast, row)))
            if count == limit:
                break


# Main program

if __name__ == '__main__':
    cli()
