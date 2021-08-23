# -*- encoding: utf-8 -*-
'''
CLSLQ is a python library and command toolsets of Connard

Most of the contents are written in progress of python learning

BSD Free License Copyright (c) Connard Lee

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

from .version import CLSLQ_Version

from .clslq_utils import mkdir_p

__all__ = [
    'SingletonClass', 'SingletonMetaclass', 'clslq_singleton'
    'ClslqConfig', 'ClslqConfigUnique', 'ClslqLogger', 'mkdir_p', 'ClslqMd5',
    'ClslqSql', 'ClslqBaseTable'
]
"""Logger wapper"""
__clslq_log = ClslqLogger()
clslog = __clslq_log.log

__version__ = CLSLQ_Version
