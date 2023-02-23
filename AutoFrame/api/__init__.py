# -*- coding: utf-8 -*-
# author:杜顺东
# time:2023/1/29 16:53
# email:my_dsd@126.com
from fastapi import APIRouter

from api.autotest.router_caseInfo_manage import router as caseInfo
from api.autotest.router_runcase_manage import router as runCase
from api.autotest.router_envinfo_manage import router as envInfo

router = APIRouter()


# 测试用例
router.include_router(caseInfo, tags=['测试用例'], prefix='/v1/qc')

#环境信息
router.include_router(envInfo, tags=['环境信息'], prefix='/v1/qc')

#环境信息
router.include_router(runCase, tags=['用例执行'], prefix='/v1/qc')