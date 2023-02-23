#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import json



class HttpRquests(object):
    def __int__(self):
        pass

    def send_post(self, url, data,):
        headers = {"authorization": "Basic bm9idWc6Z2l2ZW1lZml2ZQ=="}

        data = json.dumps(data)
        req = requests.Session()
        response_rst = req.post(url, params=data, headers=headers)
        rst = json.loads(response_rst.content)
        return rst

    def send_get(self, url, data, headers=None):
        headers = {"Content-type": "application/json;charset=UTF-8",
                   "authorization": "Basic bm9idWc6Z2l2ZW1lZml2ZQ=="}
        response_rst = requests.get(url, params=data, headers=headers)
        rst = json.loads(response_rst)
        return rst
