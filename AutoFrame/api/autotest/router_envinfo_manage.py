# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : router_envinfo_manage.py
# Time       ：2023/2/18 18:06
# Author     ：dsd
"""
from fastapi import APIRouter, Depends, Request
from common import utils
from schemas.response import responder
from sqlalchemy.orm import Session
from fastapi.params import Query
from schemas.request.autotest import envInfo_manage
from service.autotest.service_envinfo_manage import curd_env

router = APIRouter()

@router.get("/getEnvList")
async def getEnvList( db: Session = Depends(utils.get_db)):
    try:
        detail = curd_env.getEnvList(db=db)
        if detail:
            return responder.resp_2000(data=detail)
        return responder.resp_4001(data=detail, errorMsg="查询环境列表失败")
    except Exception as e:
        return responder.resp_500(data=e)

@router.get("/getEnvDetail")
async def getEnvDetail(id: int = Query(1, title="环境id"), db: Session = Depends(utils.get_db)):
    try:
        detail = curd_env.getEnvInfo(obj=id, db=db)
        if detail:
            return responder.resp_2000(data=detail)
        return responder.resp_4001(data=detail, errorMsg="查询环境信息失败")
    except Exception as e:
        return responder.resp_500(data=e)

@router.post("/createEnv")
async def createEnv(item: envInfo_manage.insetEnv, db: Session = Depends(utils.get_db)):
    try:
        detail = curd_env.insetEnv(obj=item, db=db)
        if detail:
            return responder.resp_2000(data=detail)
        return responder.resp_4001(data=detail, errorMsg="新增环境信息失败")
    except Exception as e:
        return responder.resp_500(data=e)

@router.post("/updateEnv")
async def updateEnv(item: envInfo_manage.updateEnv, db: Session = Depends(utils.get_db)):
    try:
        detail = curd_env.updateEnv(obj=item, db=db)
        if detail:
            return responder.resp_2000(data=detail)
        return responder.resp_4001(data=detail, errorMsg="更新环境信息失败")
    except Exception as e:
        return responder.resp_500(data=e)

@router.post("/deleteEnv")
async def deleteEnv(item: envInfo_manage.deleteEnv, db: Session = Depends(utils.get_db)):
    try:
        detail = curd_env.deleteEnv(obj=item, db=db)
        if detail:
            return responder.resp_2000(data=detail)
        return responder.resp_4001(data=detail, errorMsg="删除环境信息失败")
    except Exception as e:
        return responder.resp_500(data=e)