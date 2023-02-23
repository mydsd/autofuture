# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : testcase_manage.py
# Time       ：2023/2/18 21:41
# Author     ：dsd
"""

from models.base_model import Base
from sqlalchemy import Column, VARCHAR, Integer, SMALLINT, Text


class QcTestCase(Base):
    """
    测试用例表
    """
    second_level_model_name = Column(VARCHAR(255), comment="二级模块名")
    second_level_model_id = Column(Integer, comment="二级模块id")
    case_name = Column(Text, comment="用例名")
    url = Column(VARCHAR(255), comment="用例地址")
    request_method = Column(VARCHAR(255), comment="请求方式")
    save_header = Column(VARCHAR(255), comment="是否保存header")
    pre_run = Column(Text, comment="前置执行")
    request_params = Column(Text, comment="请求参数")
    skip = Column(VARCHAR(255), comment="是否跳过")
    case_assert = Column(Text, comment="响应断言")
    __table_args__ = ({'comment': '测试用例表'})
