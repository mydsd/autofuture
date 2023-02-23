# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : runCase_manage.py
# Time       ：2023/2/18 18:17
# Author     ：dsd
"""
from pydantic import BaseModel
from fastapi import Body

class CaseList(BaseModel):
    caseIdList: list = Body(None,title='用例id集合',embed=True)
    projectName: str = Body(None,title='项目名称',embed=True)
    envId: int =  Body(None,title='环境id',embed=True)
