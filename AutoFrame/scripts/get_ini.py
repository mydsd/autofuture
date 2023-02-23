# -*- coding: utf-8 -*-
# author:杜顺东
# time:2023/2/14 16:00
# email:my_dsd@126.com

import configparser
class GetConfig():
    def __init__(self,path):
        self.path = path
    def read_ini(self):
        config = configparser.ConfigParser()
        config.read(self.path,encoding='utf-8')
        return config