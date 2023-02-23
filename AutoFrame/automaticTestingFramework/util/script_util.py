import subprocess
import os,signal
from automaticTestingFramework.conf import env_conf
from automaticTestingFramework.util.operation_json import OperationJson


def run_custom_script(name, params, global_var_key):
    """
    执行自定义脚本，目前仅为python脚本
    :param name: 脚本名
    :param params: 脚本参数，多个参数为列表[param1,param2]
    :param global_var_key: 脚本执行结果存入全局变量文件的key
    :return:
    """
    script_path = os.path.join(env_conf.BASE_PATH, 'scripts', f'{name}.py')
    # if not isinstance(params, str):
    #     params = str(params)
    script_args = ["python", script_path]
    for param in params:
        if not isinstance(param, str):
            param = str(param)
        script_args.append(param)
    sub_run = subprocess.Popen(script_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = sub_run.communicate()
    status = sub_run.wait()
    #os.killpg(sub_run.pid,signal.SIGTERM)
    op_json = OperationJson(env_conf.GLOBAL_DATA_PATH)
    script_res = {}
    for line in out.splitlines():
        ret = str(line, encoding="utf8")
        op_json.write_to_global_vars(prefix='$', key=global_var_key, value=ret)
        script_res[global_var_key] = ret
    return script_res


if __name__ == '__main__':
    run_custom_script('test', [1594213390489,'aaaaaaaaaaaa'], 'AAAA')