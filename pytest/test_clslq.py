import os
import sys
from pprint import pprint

sys.path.append(os.getcwd())
from clslq import ClslqConfig
from clslq import ClslqConfigUnique
from clslq import clslog

class TestCases():
    configpath = os.path.dirname(__file__)

    '''
    Test cases for clslq logger
    '''

    def test_log(self):
        clslog.info("info")
        clslog.debug("debug")
        clslog.warn("warning")
        clslog.error("error")
        clslog.fatal("critical")

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