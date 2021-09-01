# -*- encoding: utf-8 -*-
'''
cli

click.group(name='main')

'''

import click
from click.termui import prompt
from clslq.clslq_pip import pip
from clslq.clslq_venv import venv

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(name="main", context_settings=CONTEXT_SETTINGS)
@click.version_option(message='%(prog)s-%(version)s')
def main():
    """
    CLSLQ is a python library and command toolsets of Connard.
    Most of the contents are written in progress of python learning.
    CLSLQ include some quick-start python programming functions, wrappers and tools.
    For more information, please contact [admin@lovelacelee.com].
    Documents available on https://clslq.readthedocs.io/.
    MIT License Copyright (c) Connard Lee.
    """
    pass


main.add_command(pip, name='pip')
main.add_command(venv, name='venv')

if __name__ == '__main__':
    main()
