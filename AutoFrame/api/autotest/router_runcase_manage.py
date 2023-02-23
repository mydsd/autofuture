# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : router_runcase_manage.py
# Time       ：2023/2/18 17:29
# Author     ：dsd
"""
from fastapi import APIRouter, Depends, Request
from common import utils
from schemas.response import responder
from sqlalchemy.orm import Session
from schemas.request.autotest import runCase_manage
from service.autotest.service_runcase_manage import curd_run

router = APIRouter()



@router.post("/runCase")
async def runCase(item: runCase_manage.CaseList, db: Session = Depends(utils.get_db)):
    try:
        detail = curd_run.runCase(obj=item, db=db)
        if detail:
            return responder.resp_2000(data=detail)
        return responder.resp_4001(data=detail, errorMsg="执行用例信息失败")
    except Exception as e:
        return responder.resp_500(data=e)