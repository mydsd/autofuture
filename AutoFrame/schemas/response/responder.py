"""
@Author: ljx
@File: responder.py
@Time: 2021/5/16 17:16
@Desc:
定义标准返回结果

"""

from typing import Union

from fastapi import status
from fastapi.responses import JSONResponse, Response
from fastapi.encoders import jsonable_encoder
from common import utils
def resp_2000(*, data: Union[list, dict, str] = None) -> Response:
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder({
            'success': True,
            'code': 2000,
            'data': utils.batch_hump(jsonable_encoder(data))
        })
    )


def resp_2000_page(*, data: Union[list, dict, str] = None, pageIndex, pageSize, total) -> Response:
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder({
            'success': True,
            'code': 2000,
            'data': {
                "dataSource": data,
                "pageInfo": {
                    "pageIndex": pageIndex,
                    "pageSize": pageSize,
                    "total": total
                }
            },
        })
    )


def resp_2000_false(*, data: Union[list, dict, str] = None, errorMsg: str = "") -> Response:
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder({
            'success': False,
            'code': 2000,
            'errorMsg': errorMsg,
            'data': data
        })
    )


def resp_500(*, data: Union[list, dict, str] = None, errorMsg: str = "Internal Server Error") -> Response:
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=jsonable_encoder({
            'success': False,
            'code': 500,
            'errorMsg': errorMsg,
            'data': data
        })
    )


# 请求参数格式错误
def resp_4001(*, data: Union[list, dict, str] = None,
              errorMsg: Union[list, dict, str] = "Request Validation Error") -> Response:
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder({
            'success': False,
            'code': 4001,
            'errorMsg': errorMsg,
            'data': data
        })
    )


# 用户token鉴权失败
def resp_3001(*, data: Union[list, dict, str] = None, error_msg: str = "Request Apex Fail") -> Response:
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder({
            'success': False,
            'code': 3001,
            'errorMsg': error_msg,
            'data': data
        })
    )

# 用户token过期
def resp_3002(*, data: Union[list, dict, str] = None, error_msg: str = "Token has expired") -> Response:
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder({
            'success': False,
            'code': 3002,
            'errorMsg': error_msg,
            'data': data
        })
    )


# token认证失败
def resp_4003(*, data: Union[list, dict, str] = None, errorMsg: str = "Request Fail") -> Response:
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder({
            'success': False,
            'code': 4003,
            'errorMsg': errorMsg,
            'data': data
        })
    )


# 内部验证数据错误
def resp_5002(*, data: Union[list, dict, str] = None, errorMsg: Union[list, dict, str] = "Request Fail") -> Response:
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder({
            'success': False,
            'code': 5002,
            'errorMsg': errorMsg,
            'data': data
        })
    )
