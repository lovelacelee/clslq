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
        "-q", 
        "--html=pytest/test-report.html",
        "--self-contained-html"
    ])