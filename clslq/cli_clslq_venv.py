# -*- encoding: utf-8 -*-

import click
import platform
import os
from clspy.utils import pip_conf_install
from clspy.utils import pipguess
from clspy.utils import setenv


@click.option('--create',
              '-c',
              flag_value="venv",
              help='Create python virtual environment, venv will be created.')
@click.option('--delete',
              '-d',
              flag_value="delete",
              help='Delete python virtual environment, venv will be created.')
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
def venv(create, delete, pipconf):
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

    os.system("pipenv shell")
