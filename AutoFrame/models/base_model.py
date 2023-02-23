# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : base_model.py
# Time       ：2023/2/17 19:44
# Author     ：dsd
"""
from datetime import datetime
from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, DateTime, VARCHAR
from sqlalchemy.ext.declarative import as_declarative, declared_attr, declarative_base

from common.utils import str2hump
Base = declarative_base()


@as_declarative()
class Base(Base):
    __abstract__ = True

    # 基础字段
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    create_user = Column(VARCHAR(255), comment="创建人")
    modify_user = Column(VARCHAR(255), comment="修改人")
    gmt_create = Column(DateTime, default=datetime.now, server_default=func.now(), comment="创建时间")
    gmt_modify = Column(DateTime, default=datetime.now, onupdate=datetime.now, server_default=func.now(),
                        server_onupdate=func.now(), comment="更新时间")
    deleted = Column(Integer, default=0, comment="逻辑删除:0=未删除,1=删除", server_default='0')
    db_remark = Column(VARCHAR(255), comment="数据订正记录")

    __name__: str

    @declared_attr
    def __tablename__(cls) -> str:
        import re
        # 若未指定__tablename__  则默认使用model类名转换成表名
        name_list = re.findall(r"[A-Z][a-z\d]*", cls.__name__)
        # 表名驼峰替换成下划线
        return "_".join(name_list).lower()

    # 转字典
    def to_dict(self):
        return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}

    # 转小驼峰
    def to_hump_dict(self):
        """将字段名转为以小驼峰命名

        Returns:
            [dict]: 转换后的字典数据
        """
        return {str2hump(c.name): getattr(self, c.name, None) for c in self.__table__.columns}

