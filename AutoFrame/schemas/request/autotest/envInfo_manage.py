# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : envInfo_manage.py
# Time       ：2023/2/18 18:18
# Author     ：dsd
"""
from pydantic import BaseModel
from fastapi import Body

class insetEnv(BaseModel):
    Environmental : str =  Body(None, title='环境名',embed=True)
    EnvironmentalHost : str = Body(None, title='环境host',embed=True)

class updateEnv(BaseModel):
    envId : int = Body(None, title='环境id',embed=True)
    Environmental: str = Body(None, title='环境名', embed=True)
    EnvironmentalHost: str = Body(None, title='环境host', embed=True)

class deleteEnv(BaseModel):
    envId : int = Body(None, title='环境id',embed=True)