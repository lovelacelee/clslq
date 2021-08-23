from setuptools import setup
from setuptools import find_packages
from setuptools import Command
import shutil
import os
from clslq import version

version = version.CLSLQ_Version


def match(list, s):
    if s in list:
        return True
    return False


def rmdir(path):
    removelist = [
        'build', '.pytest_cache', '__pycache__', 'clslq.egg-info', '.eggs',
        'dist'
    ]
    for root, dirs, files in os.walk(path):
        for d in dirs:
            t = os.path.join(root, d)
            father = os.path.basename(root)
            if father == '.git':
                continue
            if os.path.exists(t) and match(removelist, d):
                try:
                    print("delete {}".format(t))
                    shutil.rmtree(t, ignore_errors=True)
                except Exception as e:
                    print(e)

        for f in files:
            t = os.path.join(root, f)
            if os.path.exists(path) and match(removelist, f):
                try:
                    print("delete {}".format(t))
                    os.remove(t)
                except:
                    pass


class CleanCommand(Command):
    description = "distclean"
    user_options = []

    # This method must be implemented
    def initialize_options(self):
        pass

    # This method must be implemented
    def finalize_options(self):
        pass

    def run(self):
        workdir = os.path.dirname(os.path.abspath(__file__))
        print("distclean work root:{}".format(workdir))
        rmdir(workdir)


class DocRunCommand(Command):
    description = "doc run"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        os.system(
            "sphinx-apidoc --maxdepth 5 --separate --force -o source {} setup.py clslq.py"
            .format(os.getcwd()))
        os.system("sphinx-autobuild --host 0.0.0.0 --port 8000 source build/html")

class DocBuildCommand(Command):
    description = "doc run"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        os.system(
            "sphinx-apidoc --maxdepth 5 --separate --force -o source {} setup.py clslq.py"
            .format(os.getcwd()))
        os.system("sphinx-build -D html_theme=bizstyle -D language=zh_CN \
            -D html_logo=logo.png \
            -D html_favicon=favicon.ico \
            -a -b html ./source ./build/zh_CN")
        os.system("sphinx-build -D html_theme=bizstyle -D language=en \
            -D html_logo=logo.png \
            -D html_favicon=favicon.ico \
            -a -b html ./source ./build/en")
        shutil.copytree('source', 'docs')

class DocCreateCommand(Command):
    description = "doc create"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def sphinx_html_sidebars(self):
        with open(os.path.join('source', 'conf.py'), 'a+') as f:
            f.writelines([
                '\r\n',
                'html_sidebars = {\n',
                "'**': ['globaltoc.html', 'sourcelink.html', 'searchbox.html'],\n",
                "'using/windows': ['windowssidebar.html', 'searchbox.html'],\n",
                "}\n",

                "html_theme = 'sphinx_rtd_theme'\n"
            ])

    def run(self):
        shutil.rmtree("source", ignore_errors=True)
        shutil.rmtree(os.path.join("build", 'en'), ignore_errors=True)
        shutil.rmtree(os.path.join("build", 'zh_CN'), ignore_errors=True)
        """sphinx-quickstart create doc tree

        import os
        import sys
        sys.path.insert(0, os.path.abspath('./../'))
        html_theme = 'classic'
        extensions:sphinx.ext.napoleon
        More info @https://www.sphinx-doc.org/en/master/contents.html
        third-party theme https://sphinx-themes.org/
        official theme only clask and bizstyle are recommended

        """
        os.system(
            "sphinx-quickstart --sep {} -p CLSLQ -a Connard.Lee -v {} -r {} -l en \
            --ext-autodoc --ext-intersphinx --ext-doctest --ext-imgmath --ext-todo \
            --extensions sphinx.ext.napoleon \
            --extensions sphinx.ext.autosummary \
            --extensions sphinx.ext.githubpages \
            --extensions sphinx.ext.graphviz\
            --no-makefile --no-batchfile --no-use-make-mod --ext-coverage ".
            format(os.getcwd(), version, version))

        self.sphinx_html_sidebars()
        with open(os.path.join('source', 'conf.py'), 'a+') as f:
            f.writelines([
                '\r\n', 'import os\n', 'import sys\n',
                "sys.path.insert(0, os.path.abspath('./../'))\n"
            ])

        shutil.copyfile('logo.png', os.path.join('source', 'logo.png'))
        shutil.copyfile('favicon.ico', os.path.join('source', 'favicon.ico'))



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
            os.system(
                "twine upload --repository-url https://test.pypi.org/legacy/ dist/*"
            )
        elif self.release:
            os.system("twine upload dist/*")
        else:
            os.system(
                "twine upload --repository-url http://gw.lovelacelee.com:8002/ dist/*"
            )

        os.system("git status")
        os.system("git tag -a v{} -m 'add tag on {}'".format(version, version))
        os.system("git commit -a -m 'publish on version %s'"%version)
        os.system("git push")
        os.system("git push origin --tags")


with open('ChangeLog.md', mode='r', encoding='utf-8') as f:
    history = f.read()

setup(
    name="clslq",
    version=version,
    author="Connard.Lee",
    author_email="admin@lovelacelee.com",
    description="Connard's python library.",
    long_description=history,
    # Project home
    url="http://git.lovelacelee.com",
    install_requires=[
        'loguru',
        'Click',
        'pipenv',
        'sqlalchemy',
    ],
    platforms=["all"],
    keywords=['clslq', 'clslqutils'],
    # setup.py needs
    setup_requires=['setuptools', 'Click', 'twine', 'sphinx', 'sqlalchemy'],
    requires=['loguru'],
    # python3 setup.py test
    tests_require=[
        'pytest>=3.3.1',
        'pytest-cov>=2.5.1',
        'sqlalchemy',
        'pytest-html',
    ],
    python_requires='>=3',
    # setup_requires or tests_require packages
    # will be written into metadata of *.egg
    dependency_links=[
        #"http://gw.lovelacelee.com:8002/clslq-1.1.0.tar.gz",
    ],
    classifiers=[
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

    # setuptools.find_packages
    packages=find_packages(exclude=["pytest"]),
    package_dir={'clslq': 'clslq'},
    # Static files: config/service/pictures
    data_files=[
        # root directory such as: c:\python39\
        #('', ['conf/*.conf']),
        #('/usr/lib/systemd/system/', ['bin/*.service']),
        #('', ['clslq/pip.conf']),
        #('clslq', ['Pipfile']),
    ],
    # Will be packed
    package_data={
        'clslq': ['*.conf', '*.txt', '*.md'],
    },
    # Will not be packed
    exclude_package_data={'useless': ['*.in']},
    entry_points={'console_scripts': ["clslq = clslq.cli:main"]},
    cmdclass={
        "distclean": CleanCommand,
        "publish": PublishCommand,
        "docbuild": DocBuildCommand,
        "docrun": DocRunCommand,
        "doccreate": DocCreateCommand,
    })
