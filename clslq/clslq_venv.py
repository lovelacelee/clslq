# -*- encoding: utf-8 -*-
'''
@File    : clslq_venv
@Time    : 2021/08/21 23:47:15
@Author  : Connard Lee
@Contact : lovelacelee@gmail.com
@License : MIT License Copyright (c) 2008~2021 Connard Lee
@Desc    : Connard's python library. 
'''

import click
import platform
import os
from .clslq_utils import pip_conf_install
from .clslq_utils import pipguess
from .clslq_utils import setenv


@click.option('--create',
              '-c',
              flag_value="venv",
              help='Create python virtual environment, venv will be created.')
@click.option('--delete',
              '-d',
              flag_value="delete",
              help='Delete python virtual environment, venv will be created.')
@click.option(
    '--init',
    '-i',
    default=False,
    flag_value="init",
    help='Init dev enviroment when requirements.txt or Pipfile exists.')
@click.option('--pipconf',
              '-p',
              type=click.Path(exists=True),
              default=os.path.join(os.path.dirname(__file__), 'pip.conf'),
              help='Install pip.conf to local system, default use {}.'.format(
                  os.path.join(os.path.dirname(__file__), 'pip.conf')))
@click.command(context_settings=dict(
    allow_extra_args=True,
    ignore_unknown_options=True,
),
               help="Python venv manager of CLSLQ implement.")
def venv(create, delete, init, pipconf):
    setenv(key='PIPENV_TEST_INDEX',
           value='https://pypi.tuna.tsinghua.edu.cn/simple')
    setenv(key='WORKON_HOME', value='venv')
    if pipconf:
        pip_conf_install(pipconf)
    if create:
        click.secho("Create new environment:{}.".format(create), fg='green')
        os.system("pipenv install --three --skip-lock")
        exit()
    if delete:
        click.secho("Delete {}".format(os.path.join(os.getcwd(), 'venv')),
                    fg='green')
        os.system('pipenv --rm')
        exit()
    if init:
        requires = os.path.join(os.getcwd(), 'requirements.txt')
        if os.path.exists(requires):
            os.system(pipguess() + 'install -r %s' % requires)
        else:
            click.secho("{} is not exist.".format(requires), fg='red')

    os.system("pipenv shell")