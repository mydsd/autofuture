# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : service_caseinfo_manage.py
# Time       ：2023/2/17 21:12
# Author     ：dsd
"""
import jsonpath
from schemas.request.autotest import caseinfo_manage
from models.autotest.testcase_manage import QcTestCase
from common.logger import logger


class CRUD():
    def getCaseList(self,db):
        caseList = db.query(QcTestCase).filter(QcTestCase.deleted == 0).all()

        return caseList

    def getCaseInfo(self,obj:caseinfo_manage.GetCaseDetail,db):
        caseId = obj.caseId
        caseInfo = db.query(QcTestCase).filter(QcTestCase.id == caseId and QcTestCase.deleted == 0).all()

        return caseInfo

    def insetCase(self,obj:caseinfo_manage.insert_case,db,current_user: str = 'admin'):
        try:
            db_obj = QcTestCase(
                second_level_model_name = obj.secondLevelModelName,
                second_level_model_id = obj.secondLevelModelId,
                case_name = obj.caseName,
                url = obj.url,
                request_method = obj.requestMethod,
                save_header = obj.saveHeader,
                pre_run = obj.preRun,
                request_params = obj.requestParams,
                skip = obj.skip,
                case_assert = obj.caseAssert,
                create_user=current_user,
                modify_user=current_user,
                deleted = 0
            )
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            return {"id": db_obj.id}
        except Exception as e:
            logger.error(e)
        return False

    def updateCase(self,obj:caseinfo_manage.update_case,db,current_user: str = 'admin'):
        apiInfo_job = db.query(QcTestCase).filter(QcTestCase.id == obj.caseId).first()
        try:
            if apiInfo_job:
                apiInfo_job.second_level_model_name = obj.secondLevelModelName,
                apiInfo_job.second_level_model_id = obj.secondLevelModelId,
                apiInfo_job.case_name = obj.caseName,
                apiInfo_job.url = obj.url,
                apiInfo_job.request_method = obj.requestMethod,
                apiInfo_job.save_header = obj.saveHeader,
                apiInfo_job.pre_run = obj.preRun,
                apiInfo_job.request_params = obj.requestParams,
                apiInfo_job.skip = obj.skip,
                apiInfo_job.case_assert = obj.caseAssert,
                apiInfo_job.create_user=current_user,
                apiInfo_job.modify_user=current_user,
                db.commit()
                return {"id": apiInfo_job.id}
            else:
                return False
        except Exception as e:
            logger.error(e)
        return False
    def deleteCase(self,obj:caseinfo_manage.delete_case,db):
        db.query(QcTestCase).filter(QcTestCase.id == obj.caseId).update({QcTestCase.deleted: 1})
        db.commit()
        response_obj = {"id": obj.caseId,"msg":"用例删除成功"}
        return response_obj
curd_case = CRUD()
