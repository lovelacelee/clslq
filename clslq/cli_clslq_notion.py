# -*- encoding: utf-8 -*-
'''cli_clslq_notion

Notion client in python, notion-py is required

Usage: clslq notion [OPTIONS]


'''


import click
import platform
import pprint
import json
import re
import traceback
import xlwings as xw

from .clslq_config import ClslqConfigUnique
from .clslq_log import ClslqLogger
from notion_client import Client

clslog = ClslqLogger().log


class CellColor:
    ColorNone = -4142
    Auto = -4105
    Black = 1
    White = 2
    Red = 3
    Green = 4
    Blue = 5
    Yellow = 6
    Pink = 7
    Cyan = 8
    DarkRed = 9
    Green = 10
    DarkBlue = 11
    DarkYellow = 12
    Violet = 13
    Cyan = 14
    Gray_25 = 15
    Brown = 53,
    Olive = 52
    DarkGreen = 51
    DarkGreen_49 = 49
    Indigo = 55
    Gray_80 = 56
    Orange = 46,
    BlueGray = 47
    Gray_50 = 16
    LightOrange = 45
    AcidOrange = 43
    SeaGreen = 50
    WaterGreen = 42
    LightBlue = 41
    Gray_40 = 48
    Gold = 44
    SkyBlue = 33
    PlumRed = 54
    RoseRed = 38
    Brown = 40
    LightYellow = 36
    LightGreen = 35
    LightCyan = 34
    LightBlue = 37
    Lavender = 39


class CellVHAlignment:
    Middle = -4108
    Left = -4131
    Right = -4152
    Up = -4160
    Down = -4107
    Auto = -4130


class WorkReportXlsx(object):
    def __init__(self):
        super(WorkReportXlsx)
        self.app = xw.App(visible=False)
        self.app.display_alerts = False
        self.app.screen_updating = False
        self.wb = self.app.books.add()
        self.sht = self.wb.sheets.active

    def set_head(self, head):
        """Set sheet head

        Args:
            head (worksheet head): string
        """
        range = self.sht.range('A1:E1')
        range.merge()

        range.value = u"本周工作情况"+head.replace('-', "")
        range.color = (245, 219, 215)

        range.api.HorizontalAlignment = CellVHAlignment.Middle
        range.api.Font.Bold = True
        range.api.Font.ColorIndex = CellColor.DarkBlue

    def set_title(self):
        self.sht.range('A2').value = u"分类"
        self.sht.range('B2').value = u"进展"
        self.sht.range('C2').value = u"问题"
        self.sht.range('D2').value = u"解决"
        self.sht.range('E2').value = u"评审、复盘、总结"
        self.sht.range('A2:B2').column_width = 10
        self.sht.range('C2:E2').column_width = 30
        self.sht.range('A:E').wrap_text = True
        self.sht.range('A:E').api.HorizontalAlignment = CellVHAlignment.Middle

    def simple_wr(self, wbname, database):
        # Change sheet name
        self.sht.name = 'WR'
        self.set_head(wbname)
        self.set_title()

        self.wb.save(wbname+'.xlsx')
        self.wb.close()


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

    client = Client(auth=clsconfig.get('secrets_from'),
                    notion_version="2021-08-16")

    for i in client.search()['results']:
        # print(json.dumps(i))

        if i['object'] == 'database':
            try:
                database = client.databases.query(i['id'])
                title = i['title']
                # if title:
                for t in title:
                    plain_text = t['plain_text'].strip().replace(' → ', '~')
                    plain_text_head = t['plain_text'][0:3]
                    value = re.compile(r'^[0-9]+[0-9]$')

                    if plain_text_head == 'WRT':
                        clslog.info("Skip WRT[Work report template]")
                        break
                    if value.match(plain_text_head) == None:
                        clslog.info("Skip database which is not WR")
                        break
                    print(json.dumps(database))
                    wrp = WorkReportXlsx()
                    wrp.simple_wr(plain_text, database)
            except Exception as e:
                clslog.error(e)
                traceback.print_exc(e)
