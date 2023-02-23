# -*- coding: utf-8 -*-
# author:杜顺东
# time:2023/1/29 17:03
# email:my_dsd@126.com

from pydantic import BaseModel
from fastapi import Body

class GetCaseDetail(BaseModel):
    caseId: int = Body(None,title='用例id',embed=True)

class insert_case(BaseModel):
    secondLevelModelName : str = Body(None,title='二级模块名',embed=True)
    secondLevelModelId : int = Body(None,title='二级模块id',embed=True)
    caseName : str = Body(None,title='用例名',embed=True)
    url : str = Body(None,title='接口地址',embed=True)
    requestMethod : str = Body(None,title='接口请求方式',embed=True)
    saveHeader : str = Body(None,title='是否保存',embed=True)
    preRun : str = Body(None,title='前置执行',embed=True)
    requestParams : str = Body(None,title='请求参数',embed=True)
    skip : str = Body(None,title='是否跳过',embed=True)
    caseAssert : str = Body(None,title='响应断言',embed=True)

class update_case(BaseModel):
    caseId: int = Body(None, title='用例id', embed=True)
    secondLevelModelName: str = Body(None, title='二级模块名', embed=True)
    secondLevelModelId: int = Body(None, title='二级模块id', embed=True)
    caseName: str = Body(None, title='用例名', embed=True)
    url: str = Body(None, title='接口地址', embed=True)
    requestMethod: str = Body(None, title='接口请求方式', embed=True)
    saveHeader: str = Body(None, title='是否保存', embed=True)
    preRun: str = Body(None, title='前置执行', embed=True)
    requestParams: str = Body(None, title='请求参数', embed=True)
    skip: str = Body(None, title='是否跳过', embed=True)
    caseAssert: str = Body(None, title='响应断言', embed=True)

class delete_case(BaseModel):
    caseId: int = Body(None, title='用例id', embed=True)