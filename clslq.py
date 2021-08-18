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
from click.termui import prompt
from clslq.clslq_pip import pip
from clslq.clslq_venv import venv

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

@click.group(name="main", context_settings=CONTEXT_SETTINGS)
@click.version_option(package_name='clslq', prog_name='clslq', message='%(prog)s-%(version)s')
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
