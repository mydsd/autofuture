# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : environmental_information_manage.py
# Time       ：2023/2/17 20:21
# Author     ：dsd
"""
from models.base_model import Base
from sqlalchemy import Column, VARCHAR, Integer, SMALLINT, Text


class QcEnvironmentalInformation(Base):
    """
    一级模块表
    """
    Environmental = Column(VARCHAR(255), comment="环境名")
    Environmental_host = Column(VARCHAR(255), comment="环境地址")
    __table_args__ = ({'comment': '环境信息表'})