from automaticTestingFramework.util import script_util, find_path
from automaticTestingFramework.util.operation_excel import OperationExcel
from automaticTestingFramework.util.request_handler import RequestHandler
from jsonpath_rw import parse
import json
import re
import requests
from automaticTestingFramework.util.operation_header import OperationHeader
from automaticTestingFramework.util.operation_json import OperationJson
from automaticTestingFramework.conf import env_conf
from automaticTestingFramework.util.logger_util import logger
import datetime
from collections import defaultdict
from  automaticTestingFramework.get_eval_data.eval_data import *
from fastapi.encoders import jsonable_encoder


class RunCaseData:
    """
    加载excel测试数据 请求接口 处理依赖
    """

    def __init__(self):
        #self.opera_excel = OperationExcel()
        self.op_global_json = OperationJson(env_conf.GLOBAL_DATA_PATH)
        self.op_header_json = OperationJson(env_conf.HEADER_DATA_PATH)
        self.op_token_json = OperationJson(env_conf.Token_DATA_PATH)
        self.headers = {"content-type": "application/json"}
        self.steps = defaultdict(dict)

    def run_case(self, orgs,db,dbname,envHost):
        """
        执行接口请求，获取结果
        :return:
        """
        request = RequestHandler()
        header = self.op_header_json.data
        module_name = orgs['second_level_model_name']
        case_name = orgs['case_name']
        url = orgs['url']
        method = orgs['request_method']
        save_header = orgs['save_header']
        request_data = eval(orgs['request_params'])
        pre_run = orgs['pre_run']
        if pre_run is not None:
            pre_run_obj = eval(pre_run)
            for pre in pre_run_obj:
                pre_type = pre['pre_type']
                pre_obj = pre['pre_obj']
                key_value = pre['key_value']
                if pre_type == 1:
                    # 执行依赖用例
                    request_data = self.run_pre_case(pre_obj, orgs['id'], request_data, key_value,db,dbname,envHost)
                else:
                    request_data = self.run_pre_script(pre_obj, orgs['id'], request_data, key_value)

        # 替换url中的动态值
        if "#{" in url:
            paths = url.split('/')
            new_url = []
            for path_var in paths:
                if '#{' in path_var:
                    global_key_name = path_var[2:-1]
                    path_var = self.op_global_json.get_data(f'@{global_key_name}')
                    if not isinstance(path_var, str):
                        path_var = str(path_var)
                new_url.append(path_var)
            url = "/".join(new_url)

        if save_header is not None:
            start = datetime.datetime.now()
            res = request.send_request(method, url, request_data, self.headers,envHost)
            end = datetime.datetime.now()
            run_time = (end - start).microseconds
            op_token = OperationHeader(res)
            op_token.write_token()
            token = self.op_token_json.get_data('token')
            self.headers['token'] = token
            op_token.write_header('token', token)
        else:
            op = OperationJson()
            self.headers['token'] = op.read_data()['token']
            start = datetime.datetime.now()
            res = request.send_request(method, url, request_data, self.headers,envHost)
            end = datetime.datetime.now()
            run_time = round((end - start).microseconds,2)

        case_info = {
            "id": orgs['id'],
            "module_name": module_name,
            "case_name": case_name,
            "url": url,
            "method": method.capitalize(),
            "params": request_data,
            "response": res,
            "run_time": run_time,
            "message": ''
        }
        case_res = res
        try:
            case_res = json.loads(res)
        except:
            pass
        finally:
            return {'case_info': case_info, 'case_res': case_res}

    def get_depend_data_for_key(self, depend_case, key, case_id,db,dbname,envHost):
        """
        根据依赖的key去获取执行依赖case的响应然后返回
        :return:
        """
        pre_info = jsonable_encoder(db.query(dbname).filter(dbname.id == depend_case).all())[0]
        step_name = pre_info['case_name']
        self.steps[str(case_id)][str(depend_case)] = step_name
        step_id = len(self.steps[str(case_id)])
        logger.info(f'>>> step{step_id}: {step_name}')
        response_data = self.run_case(pre_info,db,dbname,envHost).get('case_res')
        depend_value = None
        try:
            depend_value = [match.value for match in parse(key).find(response_data)][0]
        except:
            logger.info(f'===用例Id-{case_id} 获取前置步骤依赖失败，请检查数据')
        finally:
            return depend_value

    def run_pre_script(self, script_info, row_num, request_data, key_value):
        if script_info is not None:
            # 执行脚本 并将脚本返回值写入 请求参数
            script_name = script_info[0:script_info.rfind('(')]
            script_param = re.findall(r'[(](.*?)[)]', script_info)[0].split(',')
            for sp_index in range(len(script_param)):
                if str(script_param[sp_index]).startswith('@'):
                    script_param[sp_index] = str(self.op_global_json.get_data(script_param[sp_index]))
            for key, value in key_value.items():
                find_obj = find_path.FindPathByValue(request_data)
                # 执行依赖 获取 value的值 进行替换
                script_var_paths = find_obj.in_value_path(key)
                var_in_saved = self.op_token_json.get_data(key)
                if var_in_saved is not None:
                    request_data = find_obj.update_data_by_path(script_var_paths, request_data, var_in_saved)
                else:
                    '''
                    控制台进程未关闭，取的是第一次执行函数的值
                    # 执行脚本 获得返回值
                    script_res = script_util.run_custom_script(script_name, script_param, key)
                    # 查找请求参数中的脚本变量 并替换
                    replace_value = script_res[str(key)]
                    request_data = find_obj.update_data_by_path(script_var_paths, request_data, replace_value)
                    '''
                    '''采用httprunner的lazyString进行取值'''
                    replace_value = eval_lazy_data("${%s(%s)}" % (script_name, ','.join(script_param)))
                    request_data = find_obj.update_data_by_path(script_var_paths, request_data, replace_value)
        return request_data

    def run_pre_case(self, depend_case, case_id, request_data, key_value,db,dbname,envHost):

        if depend_case is not None:
            # 获取依赖的key
            for key, value in key_value.items():
                find_obj = find_path.FindPathByValue(request_data)
                case_var_paths = find_obj.in_value_path(key)
                # 执行依赖 获取 value的值 进行替换
                # var_in_saved = self.op_global_json.get_data(key)
                # if var_in_saved is not None:
                #     request_data = find_obj.update_data_by_path(case_var_paths, request_data, var_in_saved)
                # else:
                # 获取依赖的响应数据
                depend_value = self.get_depend_data_for_key(depend_case, value, case_id,db,dbname,envHost)
                request_data = find_obj.update_data_by_path(case_var_paths, request_data, depend_value)
                # 将依赖case的返回值 写入全局变量文件-global_vars.json
                self.op_global_json.write_to_global_vars(key=key, value=depend_value)
        return request_data
