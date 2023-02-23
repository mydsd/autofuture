# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : first_level_model_manage.py
# Time       ：2023/2/17 19:48
# Author     ：dsd
"""
from models.base_model import Base
from sqlalchemy import Column, VARCHAR, Integer, SMALLINT, Text


class QcFirstLevelModel(Base):
    """
    一级模块表
    """
    first_level_model_name = Column(VARCHAR(255), comment="一级模块名")
    __table_args__ = ({'comment': '一级模块表'})