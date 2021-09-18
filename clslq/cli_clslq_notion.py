# -*- encoding: utf-8 -*-
'''cli_clslq_notion

Notion client in python

Usage: clslq notion [OPTIONS]


'''


import click
import platform
from .clslq_notion import NotionAPI
from .clslq_config import ClslqConfigUnique
from .clslq_log import ClslqLogger
from notion_client import Client

clslog = ClslqLogger().log

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

    clsconfig = ClslqConfigUnique(file=config)
    click.secho("{}".format(clsconfig.get('secrets_from')), fg='green')


    client = Client(auth=clsconfig.get('secrets_from'), notion_version="2021-08-16")

    # clslog.info(client.search()['results'])
    for i in client.search()['results']:
        if i['object'] == 'database':
            try:
                title = i['title']
                #if title:
                for t in title:
                    clslog.info(t)
            except Exception as e:
                pass
 