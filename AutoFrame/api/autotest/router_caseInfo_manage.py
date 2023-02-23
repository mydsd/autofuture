# -*- coding: utf-8 -*-
# author:杜顺东
# time:2023/1/29 17:07
# email:my_dsd@126.com
from fastapi import APIRouter, Depends,Request
from common import utils
from schemas.response import responder
from sqlalchemy.orm import Session
from schemas.request.autotest import caseinfo_manage
from service.autotest.service_caseinfo_manage import curd_case
router = APIRouter()

'''
get示例
@router.get("/getCaseInfo", summary="查询用例详情", name="查询用例详情", description="查询用例详情")
async def get_case_info(id: int = Query(1, title="用例id"),db: Session = Depends(utils.get_db)):
    try:
        case_info = curd_case.query_case_info(db, id)
        return responder.resp_2000(data=case_info)
    except Exception as e:
        return responder.resp_500(data=e)
        
'''


@router.get("/GetCaseList", summary="查询用例列表详情", name="查询用例列表详情", description="查询用例列表详情")
async def GetDetial(db: Session = Depends(utils.get_db)):
    try:
        detail = curd_case.getCaseList(db=db)
        if detail:
            return responder.resp_2000(data=detail)
        return responder.resp_4001(data=detail, errorMsg="查询用例信息失败")
    except Exception as e:
        return responder.resp_500(data=e)

@router.post("/CaseDetail")
async def CaseDetial(item: caseinfo_manage.GetCaseDetail,db: Session = Depends(utils.get_db)):
    try:
        detail = curd_case.getCaseInfo(obj=item, db=db)
        if detail:
            return responder.resp_2000(data=detail)
        return responder.resp_4001(data=detail, errorMsg="查询用例信息失败")
    except Exception as e:
        return responder.resp_500(data=e)

@router.post("/createCase")
async def createCase(item: caseinfo_manage.insert_case,db: Session = Depends(utils.get_db)):
    try:
        detail = curd_case.insetCase(obj=item, db=db)
        if detail:
            return responder.resp_2000(data=detail)
        return responder.resp_4001(data=detail, errorMsg="新建接口用例失败")
    except Exception as e:
        return responder.resp_500(data=e)

@router.post("/updateCase")
async def updateCase(item: caseinfo_manage.update_case, db: Session = Depends(utils.get_db)):
    try:
        detail = curd_case.updateCase(obj=item, db=db)
        if detail:
            return responder.resp_2000(data=detail)
        return responder.resp_4001(data=detail, errorMsg="更新用例信息失败，关键字未传")
    except Exception as e:
        return responder.resp_500(data=e)

@router.post("/deleteCase")
async def deleteCase(item: caseinfo_manage.delete_case, db: Session = Depends(utils.get_db)):
    try:
        detail = curd_case.deleteCase(obj=item, db=db)
        if detail:
            return responder.resp_2000(data=detail)
        return responder.resp_4001(data=detail, errorMsg="删除用例信息失败")
    except Exception as e:
        return responder.resp_500(data=e)