# -*- encoding: utf-8 -*-
'''
CLSLQ is a python library and command toolsets of Connard

Most of the contents are written in progress of python learning 


clslq_pip

Created: 2021/08/23 14:27:20

Contact : lovelacelee@gmail.com

MIT License Copyright (c) 2008~2021 Connard Lee

'''



import click
import platform
import os

from .clslq_utils import pipguess


@click.option(
    '--pypi',
    '-i',
    default='http://gw.lovelacelee.com:8002',
    help='The pypi mirror url, default use: http://gw.lovelacelee.com:8002')
@click.option('--trusted-host',
              '-t',
              default='gw.lovelacelee.com',
              help='The trusted mirror host, default: gw.lovelacelee.com.')
@click.command(context_settings=dict(
    allow_extra_args=True,
    ignore_unknown_options=True,
),
               help="The wrapper for pip, use local pypi as default.")
@click.pass_context
def pip(ctx, pypi, trusted_host):
    #click.echo(ctx.args)
    # upgrade pip first
    # python -m pip uninstall pip -y
    # python -m ensurepip
    # python -m pip install -U pip
    # os.system(pipguess()+'install --upgrade pip')
    _cmdline = pipguess()
    _change_pypi_cmds = ['install', 'download', 'list', 'search']
    _change_pypi = False
    for i in ctx.args:
        _cmdline += ' ' + i + ' '
        if i in _change_pypi_cmds:
            _change_pypi = True
    if _change_pypi:
        _cmdline += ' -i ' + pypi
        _cmdline += ' --trusted-host ' + trusted_host
    click.echo(_cmdline)
    click.echo('=W=H=A=T=R=E=T=U=R=N=E=D=B=Y=P=I=P=')
    os.system(_cmdline)
