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
            cls._instances[cls] = super(SingletonMetaclass, cls).__call__(*args, **kwargs)
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