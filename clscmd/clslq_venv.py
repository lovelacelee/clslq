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
from clslq.clslq_utils import pip_conf_install
from clslq.clslq_utils import pipguess
from clslq.clslq_utils import pipenv_setenv
from clslq.clslq_utils import rmdir

@click.option(
    '--create',
    '-c',
    default=False,
    help='Create python virtual environment, default ./venv will be created.'
)
@click.option(
    '--delete',
    '-d',
    default=False,
    help='Delete python virtual environment, defalt ./venv will be deleted.'
)
@click.option(
    '--init',
    '-i',
    default=False,
    help='Init dev enviroment when requirements.txt or Pipfile exists.'
)
@click.option(
    '--shell',
    '-S',
    default=True,
    help='Enter venv shell.'
)
@click.option(
    '--pipconf',
    '-p',
    type=click.Path(exists=True),
    default=os.path.join(os.path.dirname(__file__), 'pip.conf'),
    help='Install pip.conf to local system, default use {}.'.format(
        os.path.join(os.path.dirname(__file__), 'pip.conf'))
)
@click.command(
    context_settings=dict(
        allow_extra_args=True,
        ignore_unknown_options=True,
    ),
    help="Python venv manager of CLSLQ implement."
)
@click.pass_context
def venv(ctx, create, delete, init, pipconf, shell):
    pipenv_setenv()
    if pipconf:
        click.echo("pipconf:{}".format(pipconf))
        pip_conf_install(pipconf)
    if create:
        click.echo("create")
        os.system("pipenv --three")
    if delete:
        click.echo("delete {}".format(os.path.join(os.path.dirname(__file__), 'venv')))
        #rmdir(os.path.join(os.path.dirname(__file__), 'venv'))
        os.system('pipenv --rm')
        exit
    if init:
        click.echo("init:{}".format(init))
        os.system("pipenv install --three --skip-lock")
    if shell:
        os.system("pipenv --three shell")
