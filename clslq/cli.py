# -*- encoding: utf-8 -*-
'''
@File    : cli
@Time    : 2021/08/21 23:48:11
@Author  : Connard Lee
@Contact : lovelacelee@gmail.com
@License : MIT License Copyright (c) 2008~2021 Connard Lee
@Desc    : Connard's python library. 
'''

import click
from click.termui import prompt
from clslq.clslq_pip import pip
from clslq.clslq_venv import venv

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(name="main", context_settings=CONTEXT_SETTINGS)
@click.version_option(package_name='clslq',
                      prog_name='clslq',
                      message='%(prog)s-%(version)s')
def main():
    """
    CLSLQ include some quick-start python programming functions, wrappers and tools.
    For more information, please contact [admin@lovelacelee.com].
    @click: https://click-docs-zh-cn.readthedocs.io/zh/latest/
    """
    pass


main.add_command(pip, name='pip')
main.add_command(venv, name='venv')

if __name__ == '__main__':
    main()
