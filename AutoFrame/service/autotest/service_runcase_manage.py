# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : service_runcase_manage.py
# Time       ：2023/2/18 19:04
# Author     ：dsd
"""
import jsonpath
from schemas.request.autotest import runCase_manage
from models.autotest.testcase_manage import QcTestCase
from common.logger import logger
from automaticTestingFramework.util.test_runner import RunTest
from fastapi.encoders import jsonable_encoder
from service.autotest.service_envinfo_manage import curd_env
import time
class CRUD():

    def runCase(self,obj:runCase_manage.CaseList,db):
        try:

            start_time = time.time()
            end_time = time.time()
            duration = round(end_time - start_time, 2)
            caseList = obj.caseIdList
            projectName = obj.projectName
            envDetail = jsonable_encoder(curd_env.getEnvInfo(obj=obj.envId,db=db))
            envHost = envDetail[0]['Environmental_host']

            run = RunTest()
            envInfo = db.query(QcTestCase).filter(QcTestCase.id.in_(caseList)).all()
            result = run.run_cases(jsonable_encoder(envInfo),db,QcTestCase,envHost)
            #report = run.gen_report(projectName,start_time,duration)
            return result
        except Exception as e:
            logger.error(e)
        return False
curd_run = CRUD()
