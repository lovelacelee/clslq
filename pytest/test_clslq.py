# -*- encoding: utf-8 -*-
'''
@File    : test_clslq
@Time    : 2021/08/21 23:47:01
@Author  : Connard Lee
@Contact : lovelacelee@gmail.com
@License : MIT License Copyright (c) 2008~2021 Connard Lee
@Desc    : Connard's python library. 
'''

import os
import sys
from pprint import pprint
from pytest import raises
from sqlalchemy.sql.schema import Column, Table

# ignore install clslq
sys.path.insert(0, os.getcwd())
from clslq import ClslqConfig
from clslq import ClslqConfigUnique
from clslq import clslog
from clslq import ClslqSql
from clslq import ClslqBaseTable
# create sql table
from sqlalchemy import MetaData
from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String


class User(ClslqBaseTable):
    __tablename__ = 'user'
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(String(16), nullable=False, default=None)
    email_address = Column(String(60), default=None)
    nickname = Column(String(50), nullable=False, default=None)


class TestCases():
    configpath = os.path.dirname(__file__)
    '''
    Test cases for clslq logger
    '''
    def test_db(self):
        db = ClslqSql()
        db.create('sqlite:///pytest/sqlte.db')
        db.create_table(User)
        test = User(user_name='test', email_address="xx", nickname="xx")
        db.insert(test)
        db.query(User).filter(User.user_name == 'test').update(
            {'user_name': 'new'})
        db.commit()

        for i in db.query(User).all():
            clslog.info("id:{} name:{}".format(i.user_id, i.user_name))
        assert db.query(User).count() == 1
        db.delete(test)
        assert db.query(User).count() == 0

    def test_log(self):
        clslog.info("info")
        clslog.debug("debug")
        clslog.warning("warning")
        clslog.error("error")
        clslog.critical("critical")

    '''
    Test cases for clslq config parser
    '''

    def test_read(self):
        cfg = os.path.join(self.configpath, "config/server.none")
        config = ClslqConfig(cfg)
        print(cfg)
        assert config.get("key") == None

    def test_readini(self):
        inicfg = os.path.join(self.configpath, "config/server.ini")
        config = ClslqConfig(inicfg)
        print(config)
        assert config.get('Server')['name'] == 'TCPServer'

    def test_readjson(self):
        jsoncfg = os.path.join(self.configpath, "config/server.json")
        config = ClslqConfig(jsoncfg)
        print(config)
        assert config.get('name') == 'TCPServer'

    def test_readxml(self):
        xmlconfig = os.path.join(self.configpath, "config/server.xml")
        config = ClslqConfigUnique(xmlconfig)
        print(config)
        assert config.get("nodevalue").text == '4'
        assert config.get("login").attrib['username'] == 'pytest'
        assert config.get("login").attrib['password'] == '123456'
        assert config.get("login/item").attrib['attr'] == 'attr'
        assert config.get("login/item/caption").text == 'CLSLQ'

    def test_readxml_unique(self):
        xmlconfig = os.path.join(self.configpath, "config/server.xml")
        config = ClslqConfigUnique(xmlconfig)
        print(config.get("login/item/caption").text)
        assert config.get("nodevalue").text != '3'
        assert config.get("login").attrib['username'] == 'pytest'
        assert config.get("login").attrib['password'] == '123456'
        assert config.get("login/item").attrib['attr'] == 'attr'
        assert config.get("login/item/caption").text == 'CLSLQ'
        config.get("nodevalue").text = "3"
        config.get().set("nodevalue", "4")
        config.save(os.path.join(self.configpath, "config/server_dump.xml"))