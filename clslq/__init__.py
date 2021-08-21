# -*- encoding: utf-8 -*-
'''
@File    : __init__
@Time    : 2021/08/21 23:48:20
@Author  : Connard Lee
@Contact : lovelacelee@gmail.com
@License : MIT License Copyright (c) 2008~2021 Connard Lee
@Desc    : Connard's python library. 
'''

from .clslq_singleton import clslq_singleton
from .clslq_singleton import SingletonClass
from .clslq_singleton import SingletonMetaclass

from .clslq_config import ClslqConfig
from .clslq_config import ClslqConfigUnique

from .clslq_log import ClslqLogger
from .clslq_md5 import ClslqMd5
from .clslq_sql import ClslqSql
from .clslq_sql import ClslqBaseTable

from .clslq_utils import mkdir_p

__all__ = [
    'SingletonClass', 'SingletonMetaclass', 'clslq_singleton'
    'ClslqConfig', 'ClslqConfigUnique', 'ClslqLogger', 'mkdir_p', 'ClslqMd5',
    'ClslqSql', 'ClslqBaseTable'
]
"""Logger wapper"""
__clslq_log = ClslqLogger()
clslog = __clslq_log.log

__version__ = "1.1.6"