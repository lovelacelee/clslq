# CLSLQ

![img](logo.png)

CLSLQ is a python common use function library and toolsets.

Basically collect some useful functions, classes, expressions in python learning process. Why python `pypi` packages suffixed with *.wheel*? Because we are making wheels, one on the other one.

This project bootstrapped since 2021. 


# [ChangeLog](ChangeLog.md)

* Only support `python3`

# TODO

- [x] QT widgets collections
- [x] Cookiecutter intergrated
- [v] SQL database operation wapper api
- [v] Global root log wrapper
- [v] GLobal config wrapper, parser and flusher

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