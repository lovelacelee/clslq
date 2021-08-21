# -*- encoding: utf-8 -*-
'''
@File    : clslq_md5
@Time    : 2021/08/21 23:47:47
@Author  : Connard Lee
@Contact : lovelacelee@gmail.com
@License : MIT License Copyright (c) 2008~2021 Connard Lee
@Desc    : Connard's python library. 
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