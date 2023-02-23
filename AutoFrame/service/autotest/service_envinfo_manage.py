# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : service_envinfo_manage.py
# Time       ：2023/2/18 18:23
# Author     ：dsd
"""
import jsonpath
from schemas.request.autotest import envInfo_manage
from models.autotest.environmental_information_manage import QcEnvironmentalInformation
from common.logger import logger


class CRUD():
    def getEnvList(self,db):
        caseList = db.query(QcEnvironmentalInformation).filter(QcEnvironmentalInformation.deleted == 0).all()
        return caseList

    def getEnvInfo(self,obj,db):
        envInfo = db.query(QcEnvironmentalInformation).filter(QcEnvironmentalInformation.id == obj and QcEnvironmentalInformation.deleted == 0).all()
        return envInfo

    def insetEnv(self,obj:envInfo_manage.insetEnv,db,current_user: str = 'admin'):
        try:
            db_obj = QcEnvironmentalInformation(
                Environmental = obj.Environmental,
                Environmental_host = obj.EnvironmentalHost,
                create_user=current_user,
                modify_user=current_user,
                deleted = 0
            )
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            return {"id": db_obj.id,"msg":"新增环境信息成功"}
        except Exception as e:
            logger.error(e)
        return False

    def updateEnv(self,obj:envInfo_manage.updateEnv,db,current_user: str = 'admin'):
        apiInfo_job = db.query(QcEnvironmentalInformation).filter(QcEnvironmentalInformation.id == obj.envId).first()
        try:
            if apiInfo_job:
                apiInfo_job.Environmental = obj.Environmental,
                apiInfo_job.Environmental_host = obj.EnvironmentalHost,
                apiInfo_job.create_user=current_user,
                apiInfo_job.modify_user=current_user,
                db.commit()
                return {"id": apiInfo_job.id,"msg":"环境信息更新成功"}
            else:
                return False
        except Exception as e:
            logger.error(e)
        return False
    def deleteEnv(self,obj:envInfo_manage.deleteEnv,db):
        db.query(QcEnvironmentalInformation).filter(QcEnvironmentalInformation.id == obj.envId).update({QcEnvironmentalInformation.deleted: 1})
        db.commit()
        response_obj = {"id": obj.envId,"msg":"环境删除成功"}
        return response_obj
curd_env = CRUD()
