# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : test_runner.py
# Time       ：2023/2/18 21:20
# Author     ：dsd
"""
from automaticTestingFramework.util.assert_util import AssertUtil
from automaticTestingFramework.core.run_data import RunCaseData
from automaticTestingFramework.util.operation_json import init_json_data
from automaticTestingFramework.conf import env_conf
from automaticTestingFramework.util.report_util import HtmlReporter, EmailReporter
import json
import time
from automaticTestingFramework.util.logger_util import logger


class RunTest:

    def __init__(self):
        self.run = RunCaseData()
        self.assert_util = AssertUtil()

        logger.info('初始化数据准备测试环境')
        init_json_data(env_conf.GLOBAL_DATA_PATH)

        # 用于存放收集api测试结果
        self.test_results = []

    def run_cases(self,args,db,dbname,envHost):
        """程序执行"""
        pass_count = fail_count = error_count = 0
        res = None
        # 获取用例数
        rows_count = args
        # 第一行索引为0
        case_count = 0
        for i in args:
            is_run = i['skip']
            if is_run is None:
                case_count += 1
                case_id = i['id']
                case_name = i['case_name']
                logger.info(f"=======开始执行 第{case_count}条用例 >>> {case_name}")
                assert_rule = i['case_assert']
                # 接口请求
                run_res = self.run.run_case(i,db,dbname,envHost)
                case_res = run_res.get('case_res')
                case_info = run_res.get('case_info')
                logger.info(f'实际结果返回：{case_res}')

                # 结果断言
                message = ""
                assert_res = self.assert_util.get_assert_res(json.dumps(case_res), assert_rule)
                res_flag = None
                if assert_res[0] is True:
                    pass_count += 1
                    message = "sucess"
                    res_flag = True
                elif assert_res[0] is False:
                    message = "fail"
                    fail_count += 1
                    res_flag = False
                elif assert_res[0] is None:
                    message = "error"
                    error_count += 1

                case_info["assert"] = assert_res[1]
                case_info["result"] = res_flag
                case_info["message"] = message

                # 记录所有用例的测试结果
                self.test_results.append(case_info)
        logger.info(f"【测试完成】》》》用例数：{case_count}, 通过：{pass_count} 失败：{fail_count}，错误：{error_count}")
        return self.test_results

    def gen_report(self, project, start, duration):
        reporter = HtmlReporter(project=project, start=start, duration=duration, test_results=self.test_results)
        reporter.report()

    def gen_mail_report(self, project, start, duration):
        reporter = EmailReporter(project=project, start=start, duration=duration, test_results=self.test_results)
        reporter.report()
