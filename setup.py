from setuptools import setup
from setuptools import find_packages
from setuptools import Command
import shutil
import os

version='1.1.1'

def rmdir(path):
    if os.path.exists(path):
        shutil.rmtree(path)

class CleanCommand(Command):
    description = "Clean"
    user_options = []
    # This method must be implemented
    def initialize_options(self):
        pass

    # This method must be implemented
    def finalize_options(self):
        pass
    def run(self):
        workdir=os.path.dirname(os.path.abspath(__file__))
        rmdir(os.path.join(workdir, 'build'))
        rmdir(os.path.join(workdir, '.pytest_cache'))
        rmdir(os.path.join(workdir, '__pycache__'))
        rmdir(os.path.join(workdir, 'clslq.egg-info'))
        rmdir(os.path.join(workdir, 'logs'))

class PublishCommand(Command):

    description = "Publish a new version to pypi"

    user_options = [
        # The format is (long option, short option, description).
        ("test", None, "Publish to test.pypi.org"),
        ("release", None, "Publish to pypi.org"),
        ("local", None, "Publish to gw.lovelacelee.com:8002 [default]"),
    ]

    def initialize_options(self):
        """Set default values for options."""
        self.test = False
        self.release = False
        self.local = True

    def finalize_options(self):
        """Post-process options."""
        if self.test:
            print("V%s will publish to the test.pypi.org" % version)
        elif self.release:
            print("V%s will publish to the pypi.org" % version)
        else:
            print("V%s will publish to the gw.lovelacelee.com:8002" % version)

    def run(self):
        """Run command."""
        os.system("python -m pip install -U setuptools twine wheel")
        os.system("python setup.py sdist bdist_wheel")
        if self.test:
            os.system("twine upload --repository-url https://test.pypi.org/legacy/ dist/*")
        elif self.release:
            os.system("twine upload dist/*")
        else:
            os.system("twine upload --repository-url http://gw.lovelacelee.com:8002/ dist/*")

setup(
    name="clslq",
    version=version,
    author="Connard.Lee",
    author_email="lovelacelee@live.cn",
    description="Connard's python library.",
    # Project home
    url="http://lovelacelee.com",
    install_requires=['docutils>=0.3'],
    platforms=["all"],
    keywords = [
        'clslq'
    ],
    # setup.py needs
    setup_requires=[
        'pbr',
        'twine'
    ],
    requires=[
        'loguru'
    ],
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
        'Operating System :: OS Independent',
        #'Natural Language :: Chinese (Simplified)',

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
        #('', ['conf/*.conf']),
        #('/usr/lib/systemd/system/', ['bin/*.service']),
    ],
    # Will be packed
    package_data={
        '':['*.txt'],
        'bandwidth_reporter':['*.txt']
    },
    # Will not be packed
    exclude_package_data={
        'bandwidth_reporter':['*.txt']
    },
    
    cmdclass={
        "clean": CleanCommand,
        "publish": PublishCommand
    }
)