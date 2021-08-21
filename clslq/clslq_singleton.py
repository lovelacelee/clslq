# -*- encoding: utf-8 -*-
'''
@File    : clslq_singleton
@Time    : 2021/08/21 23:47:35
@Author  : Connard Lee
@Contact : lovelacelee@gmail.com
@License : MIT License Copyright (c) 2008~2021 Connard Lee
@Desc    : Connard's python library. 
'''


def clslq_singleton(cls, *args, **kv):
    """
    Define a class as a singleton class, function wrapper
    Only support __init__ function without parameters
    Usage:
        @clslq_singleton
        class Cls(object):
            def __init__(self):
                pass
    """
    _instance = {}

    def inner():
        if cls not in _instance:
            _instance[cls] = cls(*args, **kv)
        return _instance[cls]

    return inner


class SingletonClass(object):
    """
    Singleton class wapper
    Only support __init__ function without parameters
    Usage:
        class Cls(SingletonClass):
            def __init__(self):
                pass
    """
    def __new__(cls, *args, **kw):
        if not hasattr(cls, '_instance'):
            orig = super(SingletonClass, cls)
            cls._instance = orig.__new__(cls, *args, **kw)
        return cls._instance


class SingletonMetaclass(type):
    """
    Metaclass implement
    Usage:
        class Cls(metaclass=SingletonMetaclass):
            pass
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonMetaclass,
                                        cls).__call__(*args, **kwargs)
        return cls._instances[cls]


"""
Some other singleton class implement method
#--------------------------------------------------------------------
# Use __new__
#--------------------------------------------------------------------
class Single(object):
    _instance = None
    def __new__(cls, *args, **kw):
        if cls._instance is None:
            cls._instance = object.__new__(cls, *args, **kw)
        return cls._instance
    def __init__(self):
        pass
"""