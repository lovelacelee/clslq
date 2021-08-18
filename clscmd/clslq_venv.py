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
    default='venv',
    type="<url>",
    help='Create python virtual environment, default ./venv will be created.'
)

@click.option(
    '--delete',
    '-d',
    default='venv',
    help='Delete python virtual environment, default ./venv will be created.'
)

@click.option(
    '--init',
    '-i',
    default=False,
    flag_value="init",
    help='Init dev enviroment when requirements.txt or Pipfile exists.'
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
def venv(ctx, create, init, pipconf):
    click.secho(create, fg="blue")
    click.secho(init, fg="blue")
    click.secho(pipconf, fg="blue")
    if pipconf:
        pip_conf_install(pipconf)
    if create:
        click.secho("Create new {} environment.".format(create), fg='green')
        pipenv_setenv(home=create)
        os.system("pipenv install --three --skip-lock")
        exit
    else:
        click.echo("Delete {}".format(os.path.join(os.path.dirname(__file__), 'venv')))
        #rmdir(os.path.join(os.path.dirname(__file__), 'venv'))
        os.system('pipenv --rm')
        exit
    if init:
        click.echo("init:{}".format(init))
        
    os.system("pipenv shell")
