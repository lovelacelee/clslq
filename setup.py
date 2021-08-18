from setuptools import setup
from setuptools import find_packages
from setuptools import Command
import shutil
import os
import version
version=version.__version__

def match(list, s):
    for i in list:
        if i == s:
            return True
    return False
    
def rmdir(path):
    removelist = [
        'build','.pytest_cache','__pycache__','clslq.egg-info','logs','.eggs', 'dist'
    ]
    for root,dirs,files in os.walk(path):
        for d in dirs:
            t = os.path.join(root, d)
            father = os.path.basename(root)
            if father =='.git':
                continue
            if os.path.exists(t) and match(removelist, d):
                print("delete {}".format(t))
                shutil.rmtree(t)
        for f in files:
            t = os.path.join(root, f)
            if os.path.exists(path) and match(removelist, f):
                print("delete {}".format(t))
                os.remove(t)

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
        rmdir(workdir)

class PublishCommand(Command):

    description = "Publish a new version to pypi"

    user_options = [
        # The format is (long option, short option, description).
        # python setup.py --help
        ("test", 't', "Publish to test.pypi.org"),
        ("release", 'r', "Publish to pypi.org"),
        ("local", 'l', "Publish to gw.lovelacelee.com:8002 [default]"),
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
            
        os.system("git status")
        os.system("git commit -a -m 'update'")
        os.system("git push")

setup(
    name="clslq",
    version=version,
    author="Connard.Lee",
    author_email="admin@lovelacelee.com",
    description="Connard's python library.",
    # Project home
    url="http://git.lovelacelee.com",
    install_requires=[
        'loguru',
        'Click',
        'pipenv'
    ],
    platforms=["all"],
    keywords = [
        'clslq',
        'clslqutils'
    ],
    # setup.py needs
    setup_requires=[
        'setuptools',
        'Click',
        'twine'
    ],
    requires=[
        'loguru'
    ],
    # python3 setup.py test
    tests_require=[
        'pytest>=3.3.1',
        'pytest-cov>=2.5.1',
        'pytest-html'
    ],
    python_requires='>=3',
    # setup_requires or tests_require packages
    # will be written into metadata of *.egg
    dependency_links=[
        #"http://gw.lovelacelee.com:8002/clslq-1.1.0.tar.gz",
    ],

    # setuptools.find_packages
    packages=find_packages(exclude=["pytest"]),
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
        'markdown':['*.md']
    },
    # Will not be packed
    exclude_package_data={
        'useless':['*.in']
    },
    entry_points={
        'console_scripts': [
            "clslq = clscmd.cmd:main"
        ]
    },
    cmdclass={
        "distclean": CleanCommand,
        "publish": PublishCommand
    }
)