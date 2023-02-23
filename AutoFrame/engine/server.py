from fastapi import FastAPI
from api import router
from engine import load_conf
from starlette.middleware.cors import CORSMiddleware
from schemas.response import responder
import traceback

def create_app() -> FastAPI:
    """
    生成FatAPI对象
    :return:
    """
    app = FastAPI(
        debug=load_conf.debug,
        title=load_conf.title,
        description=load_conf.description,
        docs_url=load_conf.docs_url,
        openapi_url=load_conf.openapi_url,
        redoc_url=load_conf.redoc_url
    )

    # 跨域设置
    register_cors(app)

    # 注册路由
    register_router(app)
    #
    # # 注册捕获全局异常
    # register_exception(app)
    #
    # # 初始连接
    # register_init(app)
    #
    # # 请求拦截
    # register_hook(app)

    return app


def register_router(app: FastAPI) -> None:
    """
    注册路由
    :param app:
    :return:
    """
    app.include_router(router)
#
#
def register_cors(app: FastAPI) -> None:
    """
    支持跨域
    :param app:
    :return:
    """
    if load_conf.debug:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )


# def register_exception(app: FastAPI) -> None:
    """
    全局异常捕获
    TypeError: 'dict' object is not callable
    :param app:
    :return:
    """

    # 自定义异常 捕获
    # @app.exception_handler(custom_exc.TokenExpired)
    # async def user_not_found_exception_handler(request: Request, exc: custom_exc.TokenExpired):
    #     """
    #     token过期
    #     :param request:
    #     :param exc:
    #     :return:
    #     """
    #     logger.error(
    #         f"token未知用户\nURL:{request.method}{request.url}\nHeaders:{request.headers}\n{traceback.format_exc()}")
    #
    #     return responder.resp_4002(errorMsg=exc.err_desc)
    #
    # @app.exception_handler(custom_exc.TokenAuthError)
    # async def user_token_exception_handler(request: Request, exc: custom_exc.TokenAuthError):
    #     """
    #     用户token异常
    #     :param request:
    #     :param exc:
    #     :return:
    #     """
    #     logger.error(f"用户认证异常\nURL:{request.method}{request.url}\nHeaders:{request.headers}\n{traceback.format_exc()}")
    #     return responder.resp_4003(errorMsg=exc.err_desc)
    #
    # @app.exception_handler(custom_exc.AuthenticationError)
    # async def user_not_found_exception_handler(request: Request, exc: custom_exc.AuthenticationError):
    #     """
    #     用户权限不足
    #     :param request:
    #     :param exc:
    #     :return:
    #     """
    #     logger.error(f"用户权限不足 \nURL:{request.method}{request.url}")
    #     return responder.resp_4003(errorMsg=exc.err_desc)
    #
    # @app.exception_handler(ValidationError)
    # async def inner_validation_exception_handler(request: Request, exc: ValidationError):
    #     """
    #     内部参数验证异常
    #     :param request:
    #     :param exc:
    #     :return:
    #     """
    #     logger.error(
    #         f"内部参数验证错误\nURL:{request.method}{request.url}\nHeaders:{request.headers}\n{traceback.format_exc()}")
    #     return responder.resp_5002(errorMsg=exc.errors())
    #
    # @app.exception_handler(custom_exc.BusinessException)
    # async def business_exception_handler(request: Request, business_exception: custom_exc.BusinessException):
    #     logger.error(f"发生业务异常")
    #     return JSONResponse(
    #         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #         content=jsonable_encoder({
    #             'success': False,
    #             'code': business_exception.code,
    #             'errorMsg': business_exception.message,
    #             'data': None
    #         })
    #     )
    #
    # @app.exception_handler(RequestValidationError)
    # async def request_validation_exception_handler(request: Request, exc: RequestValidationError):
    #     """
    #     请求参数验证异常
    #     :param request:
    #     :param exc:
    #     :return:
    #     """
    #     logger.error(
    #         f"请求参数格式错误\nURL:{request.method}{request.url}\nHeaders:{request.headers}\n{traceback.format_exc()}")
    #     return responder.resp_4001(errorMsg=exc.errors())

    # 捕获全部异常
    # @app.exception_handler(Exception)
    # async def all_exception_handler(request: Request, exc: Exception):
    #     """
    #     全局所有异常
    #     :param request:
    #     :param exc:
    #     :return:
    #     """
    #     logger.error(f"全局异常\n{request.method}URL:{request.url}\nHeaders:{request.headers}\n{traceback.format_exc()}")
    #     return responder.resp_500()
    #
    # @app.exception_handler(custom_exc.NormalException)
    # async def unicorn_exception_handler(request: Request, exc: custom_exc.NormalException):
    #     logger.error(f"URL:{request.url}\n {traceback.format_exc()}")
    #     return responder.resp_2000_false(errorMsg=exc.message)


def register_hook(app: FastAPI) -> None:
    """
    请求响应拦截 hook
    :param app:
    :return:
    """

    # @app.middleware("http")
    # async def logger_request(request: Request, call_next) -> Response:
    #     # 接口鉴权
    #     if not request.scope.get('path') in load_conf.authentication_api_white_list:
    #         token = request.cookies.get(token_key, '').split('.')[0]
    #         k = f'c2f:token:{token}'
    #         v = redis_client_apex.get(k)
    #         if not v:
    #             logger.error(f"接口鉴权失败 {request.url}")
    #             return responder.resp_3001()
    #         res = json.loads(v)
    #         user_info = {'userName': res['accountNo'], 'name': res['name'], 'job_num': res['jobNumber']}
    #         request.state.user = user_info
    #         logger.info(f"访问记录: user: {user_info['userName']} {request.method} url:{request.url}\nheaders:{request.headers}\nIP:{request.client.host}")
    #     response = await call_next(request)
    #     return response

#def register_init(app: FastAPI) -> None:
#     """
#     初始化连接
#     :param app:
#     :return:
#     """

    # @app.on_event("startup")
    # async def init_connect():
    #     # 连接redis
    #     redis_client.init_redis_connect()
    #     redis_client_apex.init_redis_connect()
    #     # 初始化 apscheduler
    #     scheduler.init_scheduler()
    #     # 添加定时任务清理
    #     if not scheduler.get_job('cq_clean_log'):
    #         scheduler.add_job(clean_logs, id='cq_clean_log', trigger=CronTrigger.from_crontab('30 08 01 * *'))
    #     # if not scheduler.get_job('cq_sync_task'):
    #     #     scheduler.add_job(sync_task, id='cq_sync_task', trigger=CronTrigger.from_crontab('30 01 01 * *'))
    #     if not scheduler.get_job('cq_clear_sonar_project'):
    #         scheduler.add_job(clear_projects, id='cq_clear_sonar_project', trigger=CronTrigger.from_crontab('00 01 01 * *'))
        # if load_conf.cq_now_to_sync == 'true':
        #     scheduler.add_job(sync_task, id='cq_sync_task_now', trigger='date', next_run_time=datetime.now())
        #     scheduler.add_job(clear_projects, id='cq_clear_sonar_project_now', trigger='date', next_run_time=datetime.now())

        # 每天2点从repeater-console同步流量数据
        # if not scheduler.get_job('qc_traffic_sync'):
        #     scheduler.add_job(TrafficManage.sync_data, id='qc_traffic_sync', trigger=CronTrigger.from_crontab('00 02 * * *'))
        # 流量回放执行中任务进度更新
        # if not scheduler.get_job('cq_traffic_task_execute_progress'):
        #     scheduler.add_job(traffic_task_obj.get_task_execute_progress_polling_background, id='cq_traffic_task_execute_progress', trigger=CronTrigger.from_crontab('*/1 * * * *'))

    # @app.on_event('shutdown')
    # async def shutdown_connect():
    #     """
    #     关闭定时任务调度器
    #     :return:
    #     """
    #     scheduler.shutdown()
