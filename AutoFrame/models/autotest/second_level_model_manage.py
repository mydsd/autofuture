# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : second_level_model_manage.py
# Time       ：2023/2/17 20:10
# Author     ：dsd
"""
from models.base_model import Base
from sqlalchemy import Column, VARCHAR, Integer, SMALLINT, Text


class QcSecondLevelModel(Base):
    """
    二级模块表
    """
    first_level_model_id = Column(Integer, comment="二级级模块名")
    second_level_model_name = Column(VARCHAR(255), comment="二级级模块名")
    __table_args__ = ({'comment': '二级模块表'})