# -*- encoding: utf-8 -*-
'''

clslq_notion

Created: 2021/09/14 17:47:12

Contact : lovelacelee@gmail.com

MIT License Copyright (c) 2008~2021 Connard Lee

'''

import json 
import requests 
from .clslq_log import ClslqLogger

__clslq_log = ClslqLogger()
clslog = __clslq_log.log

class NotionAPI(object):
    """Notion API Implementation

    More information https://developers.notion.com/reference

    HowTo get the token: https://www.notion.so/my-integrations

    Integration type:

        Internal intergration: Only available for workspace you're an admin of. 

        Public intergration: Available for any Notion user.

    """
    def __init__(self, token):
        self.token = token
        pass
    def __repr__(self):
        return "Notion API Token: {}".format(self.token)

    def CreateDb(self):
        url = "https://api.notion.com/v1/databases/"
        pass

    def RetriveDb(self):
        pass
    def QueryDb(self):
        pass
    def UpdateDb(self):
        pass
    def CreatePage(self):
        pass
    
    def UpdatePage(self):
        pass
    
    def DeletePage(self):
        pass
    def RetriveBlock(self):
        pass
    def UpdateBlock(self):
        pass
    def RetriveBlockChildren(self):
        pass
    def AppendBlockChildren(self):
        pass
    def DeleteBlock(self):
        pass