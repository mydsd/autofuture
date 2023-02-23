'''
Author       : xuzhu.zzp
Date         : 2021-11-24 13:39:17
Description  : 流量管理相关接口响应封装
'''

from datetime import datetime
from pydantic import BaseModel, Field
from typing import List, Optional, Text
from enum import Enum, unique

class PagesInfo(BaseModel):
    total: int = Field(..., title='总数')
    pageSize: int = Field(..., title='每页条数')
    pageIndex: int = Field(..., title='当前页')

class CaseBase(BaseModel):
    title: str = Field(..., title='标题', description='用例标题')

class Traffic(CaseBase):
    id: int = Field(..., title='用例id', description='用例id') 
    priority: str = Field(..., title='优先级', description='用例优先级')
    categoryId: int = Field(..., title='所属类目id', description='所属类目id')
    createUser: str = Field(..., title='创建者', description='创建者')
    gmtCreate: datetime = Field(..., title='创建时间', description='创建时间')
    gmtModify: datetime = Field(..., title='修改时间', description='修改时间')

class CaseListResponse(CaseResponseBase):
    categoryName: str =  Field(..., title='所属类目名')
class CasePageListResponse(BaseModel):
    dataSource: List[CaseListResponse] = Field(..., title='用例列表')
    pageInfo: PagesInfo = Field(..., title='分页页码信息')
