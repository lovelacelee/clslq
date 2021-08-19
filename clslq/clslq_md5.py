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

import hashlib

class ClslqMd5(object):
    def __init__(self) -> None:
        super().__init__()

    def __repr__(self) -> str:
        return super().__repr__()

    def file(self, filename):
        '''
        :param filename:
        :return: md5 string
        '''
        m = hashlib.md5()
        with open(filename, 'rb') as f:
            while True:
                data = f.read(4096)
                if not data:
                    break
                m.update(data)
        return m.hexdigest()

    def string(self, content):
        '''
        :param content:
        :return: md5 string
        '''
        m = hashlib.md5(content)
        return m.hexdigest()

    def same(self, f1, f2):
        '''
        :param f1: first filename or content<string>
        :param f2: second filename or content<string>
        :return: True if md5(f1) == md5(f2)
        '''
        if type(f1) == type(str) == type(f2):
            md51 = self.string(f1)
            md52 = self.string(f2)
        else:
            md51 = self.file(f1)
            md52 = self.file(f2)
        return md51 == md52