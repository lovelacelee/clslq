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
from .clslq_singleton import clslq_singleton
from .clslq_singleton import SingletonClass
from .clslq_singleton import SingletonMetaclass

from .clslq_config import ClslqConfig
from .clslq_config import ClslqConfigUnique

from .clslq_log import ClslqLogger

from .clslq_utils import mkdir_p

__all__ = [
    'SingletonClass', 'SingletonMetaclass', 'clslq_singleton'
    'ClslqConfig', 'ClslqConfigUnique',
    'ClslqLogger',
    'mkdir_p'
]

"""Logger wapper"""
__clslq_log = ClslqLogger()
clslog = __clslq_log.log

__version__ = "1.1.3"