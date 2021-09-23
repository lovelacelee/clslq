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
import os
import re
import traceback
import pandas
# Support email
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header

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


class Report(object):
    """Base class of Report

    Args:
        object (wbname): Workbook name
    """

    def __init__(self, wbname):
        self.wb = Workbook()
        self.sht = self.wb.active
        self.default_border = Border(left=Side(border_style='thin', color='000000'),
                                     right=Side(border_style='thin',
                                                color='000000'),
                                     top=Side(border_style='thin',
                                              color='000000'),
                                     bottom=Side(border_style='thin', color='000000'))
        self.wbname = wbname

    def render_html(self, title):
        df = pandas.read_excel(self.wbname+'.xlsx', sheet_name='WR', header=1)
        pandas.set_option('colheader_justify', 'center')

        df.style.hide_index()  # Hide index col

        #df.to_html(wbname+'.html', index=False, na_rep="", border=1)
        with open(self.wbname+'.html', encoding='utf-8', mode='w') as f:
            f.write("""<html><head><title>""")
            f.write(title)
            f.write("""</title></head>
            <style>
                .tablestyle {
                    font-size: 11pt;
                    font-family: Arial;
                    border-collapse: collapse;
                    border: 1px solid silver;
                }
                .tablestyle td
                {
                    width: 300px;
                }
                .tablestyle td:nth-child(1)
                {
                    width: 80px;
                    text-align: center;
                }
                .tablestyle td:nth-child(3)
                {
                    width: 60px;
                    text-align: center;
                }
                .tablestyle td, th {
                    padding: 5px;
                }
                .tablestyle tr:nth-child(even) {
                    background: #E0E0E0;
                }
                .tablestyle th {
                    background: #ff8936;
                }
                .tablestyle tr:hover {
                    background: silver;
                    cursor: pointer;
                }
            </style>
            <body>
            """)
            f.write(df.to_html(classes='tablestyle', index=False, na_rep=""))
            f.write("""</body></html>""")

    def send_email(self, config, title):
        email = config.get('email')
        smtpserver = email['sender']['smtpserver']
        user = email['sender']['user']
        pwd = email['sender']['pwd']
        receivers = email['receivers']
        clslog.info("{} {} {}".format(smtpserver, user, title))

        msg = MIMEMultipart()
        msg['From'] = "{}".format(user)
        msg['To'] = ",".join(receivers)
        msg['Subject'] = Header(title, 'utf-8')
        with open(self.wbname+'.html', "r", encoding='utf-8') as f:
            msg.attach(MIMEText(f.read(), 'html', 'utf-8'))
        try:
            smtp = smtplib.SMTP()
            smtp.connect(smtpserver)
            smtp.login(user, pwd)
            smtp.sendmail(user, receivers, msg.as_string())
            clslog.info('Email sent to {} done'.format(receivers))
            smtp.quit()
            smtp.close()
        except Exception as e:
            clslog.critical(e)

    def remove_files(self):
        os.remove(self.wbname+'.html')
        os.remove(self.wbname+'.xlsx')


class WeekReport(Report):

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
            return result.replace('\n', ' ')

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

    def dump(self, wbname, database):
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


@click.option('--week',
              '-w',
              flag_value='month',
              help='Generate week report form notion account data')
@click.option('--month',
              '-m',
              flag_value='month',
              help='Generate month report form notion account data')
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
def notion(week, month, config):
    clsconfig = ClslqConfigUnique(file=config)
    if clsconfig.get('secrets_from') is None:
        click.secho(
            "Make sure notion secret code is valid in .clslq.json", fg='red')
        return

    client = Client(auth=clsconfig.get('secrets_from'),
                    notion_version="2021-08-16")

    click.secho("Notion Accounts:", fg='yellow')
    for u in client.users.list()['results']:
        click.secho("{:8s} {}".format(u['name'], u['id']), fg='green')
    if week:
        click.secho("Week report search", fg='green')
        for i in client.search()['results']:
            if i['object'] == 'database':
                try:
                    database = client.databases.query(i['id'])
                    title = i['title']

                    for t in title:
                        plain_text = t['plain_text'].strip().replace(
                            ' → ', '~')
                        plain_text_head = t['plain_text'][0:3]
                        value = re.compile(r'^[0-9]+[0-9]$')

                        if plain_text_head == 'WRT':
                            break
                        if value.match(plain_text_head) == None:
                            break
                        wrp = WeekReport(plain_text)
                        wrp.dump(plain_text, database)
                        wtitle = "{}({})".format(
                            clsconfig.get('wr_title_prefix'), plain_text)
                        wrp.render_html(wtitle)
                        wrp.send_email(clsconfig, wtitle)
                        # wrp.remove_files()

                except Exception as e:
                    clslog.error(e)
                    traceback.print_exc(e)

    else:
        click.secho("Month report search", fg='green')
        mtitle = config['mr_title_prefix']
