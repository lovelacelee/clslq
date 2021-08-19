# -*- encoding:utf-8 -*-
'''
MIT License

Copyright (c) 2021 Connard Lee

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''
import click
import platform
import os

from .clslq_utils import pipguess

@click.option(
    '--pypi',
    '-i',
    default='http://gw.lovelacelee.com:8002',
    help='The pypi mirror url, default use: http://gw.lovelacelee.com:8002'
)
@click.option(
    '--trusted-host',
    '-t',
    default='gw.lovelacelee.com',
    help='The trusted mirror host, default: gw.lovelacelee.com.'
)
@click.command(
    context_settings=dict(
        allow_extra_args=True,
        ignore_unknown_options=True,
    ),
    help="The wrapper for pip, use local pypi as default."
)
@click.pass_context
def pip(ctx, pypi, trusted_host):
    #click.echo(ctx.args)
    # upgrade pip first
    # python -m pip uninstall pip -y
    # python -m ensurepip
    # python -m pip install -U pip
    # os.system(pipguess()+'install --upgrade pip')
    _cmdline = pipguess()
    _change_pypi_cmds = [ 'install', 'download', 'list', 'search']
    _change_pypi = False
    for i in ctx.args:
        _cmdline += ' ' + i + ' '
        if i in _change_pypi_cmds:
            _change_pypi = True
    if _change_pypi:
        _cmdline += ' -i '+pypi
        _cmdline += ' --trusted-host '+trusted_host
    click.echo(_cmdline)
    click.echo('=W=H=A=T=R=E=T=U=R=N=E=D=B=Y=P=I=P=')
    os.system(_cmdline)
