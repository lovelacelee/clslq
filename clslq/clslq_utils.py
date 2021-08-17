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
import os
import sys
import platform
import re
import shutil

def mkdir_p(file):
    path = file
    if file.find('/') or file.find('\\') > 0:
        path = os.path.dirname(file)
    if not os.path.exists(path):
        os.makedirs(path, 0o777)

def dir_copy(srcpath, dstpath):
    try:
        if not os.path.exists(srcpath):
            return
        if not os.path.exists(dstpath):
            if sys.version_info.major >= 3 and sys.version_info.minor >= 8:
                shutil.copytree(srcpath, dstpath, dirs_exist_ok=True)
            else:
                shutil.copytree(srcpath, dstpath)
    except Exception as e:
        pass

def win_runtime_cp(src, to):
    # useful while running a package by pyinstaller on windows
    if platform.system() == "Windows":
        for path in sys.path:
            if re.match(r'^_MEI\d+$', os.path.basename(path)):
                if os.path.exists(path):
                    dir_copy(src, to)
                    break
def is_frozen():
    # All of the modules are built-in to the interpreter, e.g., by py2exe
    return hasattr(sys, "frozen")