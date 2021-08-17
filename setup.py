from setuptools import setup
from setuptools import find_packages

setup(
    name="clslq",
    version="1.0.0",
    author="Connard.Lee",
    author_email="lovelacelee@live.cn",
    description="Connard's python library.",
    # Project home
    url="http://lovelacelee.com",
    install_requires=['docutils>=0.3'],
    # setup.py needs
    setup_requires=['pbr'],
    # python3 setup.py test
    tests_require=[
        'pytest>=3.3.1',
        'pytest-cov>=2.5.1',
    ],
    python_requires='>=3',
    # setup_requires or tests_require packages
    # will be written into metadata of *.egg
    dependency_links=[
        #"http://example2.com/p/foobar-1.0.tar.gz",
    ],

    # setuptools.find_packages
    packages=find_packages(),
    classifiers = [
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 5 - Production/Stable',

        # Target users
        'Intended Audience :: Developers',

        # Project type
        'Topic :: Software Development :: Build Tools',

        'License :: OSI Approved :: MIT License',

        # Target Python version
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],

    # Static files: config/service/pictures
    data_files=[
        ('', ['conf/*.conf']),
        ('/usr/lib/systemd/system/', ['bin/*.service']),
    ],
    # Will be packed
    package_data={
        '':['*.txt'],
        'bandwidth_reporter':['*.txt']
    },
    # Will not be packed
    exclude_package_data={
        'bandwidth_reporter':['*.txt']
    }
)