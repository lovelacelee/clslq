# CLSLQ

![img](logo.png)

CLSLQ is a python common use function library and toolsets.

Basically collect some useful functions, classes, expressions in python learning process. Why python `pypi` packages suffixed with *.wheel*? Because we are making wheels, one on the other one.

This project bootstrapped since 2021. 


# [ChangeLog](ChangeLog.md)

* Only support `python3`

# TODO

- [ ] QT widgets collections
- [ ] Cookiecutter intergrated
- [x] SQL database operation wapper api
- [x] Global root log wrapper
- [x] GLobal config wrapper, parser and flusher

# How-To

Here is for the lost memory:

## Use clslq command toolsets

```
$ pip3 install clslq -U
$ clslq --version
$ clslq --help
```

## Running test cases

```
$ pip3 install pytest pytest-html
$ pip3 install -U -r requirements/dev.txt
$ pip3 install -U -r requirements/prod.txt
$ python3 pytest
```

## Develop environment build 

```
$ python3 setup.py venv init
(clslq-RJvATSUq)$ python3 setup.py doc
```

setup.py help

```
$ python3 setup.py --help
$ python3 setup.py --help-commands
```

build doc
```
$ python3 setup.py builddoc
$ python3 setup.py rundoc
```

publish project to pypi or local pypi

```
$ python3 setup.py publish
$ python3 setup.py distclean
```

## Install to system or just for specified user

for user

```
python3 install clslq --user
python3 -m clslq.cli --help
```
