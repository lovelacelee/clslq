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

import sys
import logging
from logging import critical, handlers, info
from .clslq_singleton import SingletonClass
from .clslq_utils import mkdir_p

class ClslqLogger(SingletonClass):
    _logfile = None
    _filehdr = None
    _loglevel = logging.DEBUG
    _root_logger = logging.RootLogger(logging.DEBUG)
    _fmtstring = '[%(levelname)-8.8s %(asctime)s %(filename)s:%(lineno)d] %(message)s'
    def __init__(self, file=None) -> None:
        super().__init__()
        self._logfile = file
        self._root_logger.handlers.clear()
        '''Console'''
        console = logging.StreamHandler()
        console.setLevel(self._loglevel)
        console.setFormatter(logging.Formatter(self._fmtstring))
        self._root_logger.addHandler(console)
        """
        Instance of TimedRotatingFileHandler
        interval: interval
        backupCount: delete log file more then backupCount files
        when: S-Seconds M-Miniutes H-Hours D-Days W-Weeks(==0 means monday) midnight(00:00)
        """
        if self._logfile:
            mkdir_p(self._logfile)
            self._filehdr = handlers.TimedRotatingFileHandler(self._logfile, 
                backupCount=3, when='D', encoding='utf-8')
            self._filehdr.setFormatter(logging.Formatter(self._fmtstring))
            self._filehdr.setLevel(self._loglevel)
            self._root_logger.addHandler(self._filehdr)

    @property
    def log(self, filename=None):
        try:
            '''pip install logru'''
            from loguru import logger
            if filename:
                logger.add(
                    "logs/app.log",
                    rotation="2 days",
                    retention="14",
                    format='[{time:YYYY-MM-DD HH:mm:ss} |{level:8.8s}| {file}:{line}]{message}',
                    encoding='utf-8', enqueue=True
                )
            logger.add(
                sys.stderr,
                format='[<green>{time:YYYY-MM-DD HH:mm:ss}</green> |{level:8.8s}| {file}:<green>{line}</green>]{message}',
                encoding='utf-8', enqueue=True, colorize=True
            )
            return logger
        except:
            return ClslqLogger._root_logger

    @property
    def file(self):
        return self._logfile
    @file.setter
    def file(self, path):
        self._logfile = path


