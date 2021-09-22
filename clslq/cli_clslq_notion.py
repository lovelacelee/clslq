# -*- encoding: utf-8 -*-
'''cli_clslq_notion

Notion client in python, notion-py is required

Usage: clslq notion [OPTIONS]

[openpyxl](https://openpyxl-chinese-docs.readthedocs.io/zh_CN/latest/tutorial.html)

'''


import click
import platform
import pprint
import json
import re
import traceback
from openpyxl import Workbook
from openpyxl.styles import Font
from openpyxl.styles import colors
from openpyxl.styles import Alignment
from openpyxl.styles import Border
from openpyxl.styles import Side
from openpyxl.styles import PatternFill

from .clslq_config import ClslqConfigUnique
from .clslq_log import ClslqLogger
from notion_client import Client

clslog = ClslqLogger().log


class WorkReportXlsx(object):
    def __init__(self):
        super(WorkReportXlsx)
        self.wb = Workbook()
        self.sht = self.wb.active
        self.default_border = Border(left=Side(border_style='thin', color='000000'),
                                     right=Side(border_style='thin',
                                                color='000000'),
                                     top=Side(border_style='thin',
                                              color='000000'),
                                     bottom=Side(border_style='thin', color='000000'))

    def set_head(self, head):
        """Set sheet head

        Args:
            head (worksheet head): string
        """
        self.sht.merge_cells('A1:F1')

        self.sht['A1'] = u"本周工作情况"+head.replace('-', "")
        self.sht['A1'].alignment = Alignment(
            horizontal='center', vertical='center')
        self.sht['A1'].font = Font(
            color=colors.BLACK, b=True, size=14)
        self.sht['A1'].fill = PatternFill("solid", fgColor="00FF8080")
        self.sht.row_dimensions[1].height = 20

    def set_title(self):
        u"""openpyxl 不支持按列设置样式
        """
        self.sht['A2'] = u"分类"
        self.sht['B2'] = u"事项"
        self.sht['C2'] = u"进展"
        self.sht['D2'] = u"问题"
        self.sht['E2'] = u"解决"
        self.sht['F2'] = u"评审、复盘、总结"
        for col in range(1, 7):
            self.sht.cell(column=col, row=2).font = Font(
                name=u'微软雅黑', bold=True, size=12)

    def content_parse_title(self, item):
        result = None
        try:
            title = item[u'名称']['title']
            for i in title:
                result = i['plain_text']
        except Exception as e:
            pass
        finally:
            return result

    def content_parse_state(self, item, row):
        result = ''
        try:
            for i in item[u'状态']['multi_select']:
                if i['name'] == u'进行中':
                    for col in range(1, 7):
                        self.sht.cell(column=col, row=row).fill = PatternFill(
                            "solid", fgColor="00CCFFCC")
                if i['name'] == u'遇问题':
                    for col in range(1, 7):
                        self.sht.cell(column=col, row=row).fill = PatternFill(
                            "solid", fgColor="00FFCC99")
                result = "{} {}".format(result, i['name'])
        except Exception as e:
            pass
        finally:
            return result

    def content_parse_type(self, item, row):
        result = ''
        try:
            result = item[u'分类']['select']['name']
            if result == u'工作计划':
                self.sht.cell(column=6, row=row).value = u"下周工作计划"
                for col in range(1, 7):
                    self.sht.cell(column=col, row=row).fill = PatternFill(
                        "solid", fgColor="00CCFFCC")
        except Exception as e:
            pass
        finally:
            return result

    def content_parse_richtext(self, item, text):
        result = ''
        try:
            title = item[text]['rich_text']
            for i in title:
                result = i['plain_text']
        except Exception as e:
            pass
        finally:
            return result

    def content_fill(self, item, row):
        self.sht['A'+str(row)] = self.content_parse_type(item, row)
        self.sht['B'+str(row)] = self.content_parse_title(item)
        self.sht['C'+str(row)] = self.content_parse_state(item, row)
        self.sht['D'+str(row)] = self.content_parse_richtext(item, u'问题')
        self.sht['E'+str(row)] = self.content_parse_richtext(item, u'解决方法')
        self.sht['F'+str(row)] = self.content_parse_richtext(item, u'评审、复盘、总结')

        for c in ('A', 'C'):
            self.sht.column_dimensions[c].width = 10
            for cell in self.sht[c]:
                cell.alignment = Alignment(
                    horizontal='center', vertical='center', wrap_text=True)
                cell.border = self.default_border
        for c in ('B', 'F', 'D', 'E'):
            self.sht.column_dimensions[c].width = 30
            for cell in self.sht[c]:
                cell.alignment = Alignment(
                    horizontal='center', vertical='center', wrap_text=True)
                cell.border = self.default_border

    def simple_wr(self, wbname, database):
        # Change sheet name
        self.sht.title = 'WR'
        self.set_head(wbname)
        self.set_title()

        # print(json.dumps(database))
        row = 3
        for node in database['results']:
            item = node['properties']
            self.content_fill(item, row)
            row = row + 1
        self.wb.save(filename=wbname+'.xlsx')
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
                    wrp = WorkReportXlsx()
                    wrp.simple_wr(plain_text, database)
            except Exception as e:
                clslog.error(e)
                traceback.print_exc(e)
