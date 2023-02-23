import json
from jsonpath_rw import parse
from automaticTestingFramework.conf import env_conf
from automaticTestingFramework.util.logger_util import logger
from automaticTestingFramework.util.operation_json import OperationJson


class AssertUtil:
    op_global_json = OperationJson(env_conf.GLOBAL_DATA_PATH)

    def get_assert_res(self, actual_res, assert_rule):
        """
        测试结果断言
        :param actual_res:实际结果
        :param assert_rule:断言规则
                        [{"desc":"验证是否获取时间成功",
                        "assert_way":"response",
                        "compare_obj":"${resp}",
                        "compare_way":"contain"，
                        "expect":"Time"
                        }]
        :return:
        """

        res_dict = json.loads(actual_res)
        flag = False
        assert_res = ''
        assert_res_list = []

        try:
            assert_rule_obj = eval(assert_rule)

            if not isinstance(assert_rule_obj, list):
                flag = False
            else:
                assert_content_list = []
                for rule in assert_rule_obj:
                    assert_desc = rule['desc']
                    assert_way = rule['assert_way']
                    compare_way = rule['compare_way']
                    compare_obj = rule['compare_obj']
                    expect = rule['expect']
                    if isinstance(expect, str) and '@{' in expect:
                        expect = self.op_global_json.get_data(expect)

                    if compare_obj == '${resp}':
                        compare_obj = '返回结果'

                    if assert_way == 'response':
                        if compare_way == 'contain':
                            flag = expect in actual_res
                    elif assert_way == 'jsonPath':
                        actual_field_value = [match.value for match in parse(compare_obj).find(res_dict)][0]
                        if compare_way == '=':
                            flag = actual_field_value == expect
                        elif compare_way == '!=':
                            flag = actual_field_value != expect
                        elif compare_way == '>':
                            flag = actual_field_value > expect
                        elif compare_way == '<':
                            flag = actual_field_value > expect
                        else:
                            flag = False
                    else:
                        flag = False

                    # assert_content = f'验证: {compare_obj} {compare_way} {expect},结果：{flag}'
                    # assert_content_list.append(assert_content)
                    assert_res_list.append({'desc': assert_desc, 'expect': f'{compare_obj} {compare_way} {expect}', 'res': flag})

                # assert_res = '\r\n'.join(assert_content_list)
        except Exception as e:
            logger.error('断言内容解析异常')
            flag = False

        return flag, json.dumps(assert_res_list, sort_keys=True, ensure_ascii=False)



