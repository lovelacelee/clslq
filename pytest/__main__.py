# -*- encoding: utf-8 -*-
'''
@File    : __main__
@Time    : 2021/08/21 23:47:08
@Author  : Connard Lee
@Contact : lovelacelee@gmail.com
@License : MIT License Copyright (c) 2008~2021 Connard Lee
@Desc    : Connard's python library. 
'''

import os
import pytest

if __name__ == '__main__':
    """
    How to run pytest cases:
        cd ..
        python pytest
    """
    pytest.main([
        os.path.join(os.path.dirname(__file__), 'test_clslq.py'),
        #"-q",
        "-v",
        "--capture=sys",
        "--html=pytest/test-report.html",
        "--self-contained-html"
    ])