# -*- encoding: utf-8 -*-



import os
import sys
import json
import configparser
import traceback
from enum import Enum
from xml.etree import ElementTree as ET

from .clslq_singleton import SingletonMetaclass

try:
    '''pyyaml package is required'''
    import yaml
except Exception as e:
    traceback.format_exc()


class ClslqConfigType(Enum):
    CCJson = 1
    CCYaml = 2
    CCIni = 3
    CCXml = 4


class ClslqConfig(object):
    """
    ClslqConfig is a config manager
    Aim to support json/xml/ini/yaml to dict manager
    """
    _filepath = None
    _execpath = None
    '''
    Json: object as dict
    Ini: object as dict
    Xml: ElementTree object
    Yaml: object as dict
    '''
    _config = None
    '''ClslqConfig type'''
    _type = ClslqConfigType.CCJson
    '''Only valid as xml config'''
    _tree = None

    def __init__(self, file="config.json") -> None:
        self._filepath = os.path.dirname(os.path.abspath(__file__))
        self._execpath = os.path.dirname(os.path.abspath(sys.argv[0]))
        sys.path.append(self._filepath)
        sys.path.append(self._execpath)
        self.load(file)

    def __repr__(self) -> str:
        return '<ClslqConfig[{} @{}@{}] {}>'.format(self._type, self._filepath,
                                                    self._execpath,
                                                    self._config)

    def _guess_suffix(self, file):
        try:
            suffix = os.path.splitext(file)[-1]
        except:
            pass
        if suffix == '.json':
            return ClslqConfigType.CCJson
        elif suffix == '.yaml':
            return ClslqConfigType.CCYaml
        elif suffix == '.ini':
            return ClslqConfigType.CCIni
        elif suffix == '.xml':
            return ClslqConfigType.CCXml
        else:
            return None

    def get(self, key=None):
        '''Return json object'''
        try:
            if self._type == ClslqConfigType.CCXml:
                if key:
                    return self._config.find(key)
            elif self._type == ClslqConfigType.CCJson or \
                self._type == ClslqConfigType.CCIni or \
                self._type == ClslqConfigType.CCYaml:
                return self._config[key]
            return self._config
        except Exception as e:
            # print("ClslqConfig get '{}' failed[{}]".format(key, e))
            # traceback.print_exc()
            pass

    def load(self, file):
        self._type = self._guess_suffix(file)
        try:
            if self._type == ClslqConfigType.CCIni:
                self._config = configparser.ConfigParser()
                self._config.read(file)
            elif self._type == ClslqConfigType.CCXml:
                self._tree = ET.parse(file)
                self._config = self._tree.getroot()
            else:
                with open(file, 'r', encoding="utf-8") as fp:
                    if self._type == ClslqConfigType.CCJson:
                        self._config = json.load(fp)
                    elif self._type == ClslqConfigType.CCYaml:
                        fdata = fp.read()
                        self._config = yaml.safe_load(fdata)
                    else:
                        raise Exception.args("Not supported")
        except Exception as e:
            #print(e)
            pass
        finally:
            #print(self._config)
            pass

    def save(self, file):
        savetype = self._guess_suffix(file)
        if self._type != savetype:
            return False
        try:
            if self._type == ClslqConfigType.CCIni:
                self._config.write(file)
            elif self._type == ClslqConfigType.CCXml:
                self._tree.write(file, encoding='utf-8', xml_declaration=True)
            else:
                with open(file, 'r', encoding="utf-8") as fp:
                    if self._type == ClslqConfigType.CCJson:
                        json.dump(self._config, fp, indent=4)
                    elif self._type == ClslqConfigType.CCYaml:
                        yaml.dump(self._config, file)
                    else:
                        raise Exception.args("Not supported")
        except Exception as e:
            #print(e)
            pass


class ClslqConfigUnique(ClslqConfig, metaclass=SingletonMetaclass):
    pass