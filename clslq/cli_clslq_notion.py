# -*- encoding: utf-8 -*-
'''cli_clslq_notion

Notion client in python

Usage: clslq notion [OPTIONS]


'''


import click
import platform
import os
from .clslq_notion import NotionAPI
from .clslq_config import ClslqConfigUnique


@click.option('--verbose',
              '-v',
              flag_value="verbose",
              help='Echo information when notion response.')

@click.option('--config',
              '-c',
              type=click.Path(exists=True),
              default='.clslq.json',
              help='CLSLQ config use {} as default.'.format('.clslq.json'))
@click.command(context_settings=dict(
    allow_extra_args=True,
    ignore_unknown_options=True,
),
    help="Notion API beta.")
def notion(verbose, config):
    click.secho("{}, {}".format(verbose, config), fg='green')
    clsconfig = ClslqConfigUnique(file=config)
    click.secho("{}".format(clsconfig.get('secrets_from')))
