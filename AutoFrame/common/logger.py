"""
@Author: ljx
@File: logger.py
@Time: 2021/5/16 17:35
@Desc:
日志配置

"""

import os, time
from loguru import logger
from engine.load_conf import base_path

# 日志目录
log_dir = os.path.join(base_path, 'logs')
if not os.path.exists(log_dir):
    os.mkdir(log_dir)

# 函数产生的代码目录
code_dir = os.path.join(base_path, 'code')
if not os.path.exists(code_dir):
    os.mkdir(code_dir)

# 代码目录-自动化脚本
automation_script_dir = os.path.join(code_dir, 'automation')
if not os.path.exists(automation_script_dir):
    os.mkdir(automation_script_dir)

# api服务日志目录
log_path = os.path.join(log_dir, 'api-service')
if not os.path.exists(log_path):
    os.mkdir(log_path)

# 自动化执行日志目录
automation_log_dir = os.path.join(log_dir, 'automation')
if not os.path.exists(automation_log_dir):
    os.mkdir(automation_log_dir)

# 自动化报告目录
automation_report_dir = os.path.join(automation_log_dir, 'reports')
if not os.path.exists(automation_report_dir):
    os.mkdir(automation_report_dir)

# 单测报告执行目录
unittest_report_dir = os.path.join(log_dir, 'unittest')
if not os.path.exists(unittest_report_dir):
    os.mkdir(unittest_report_dir)



log_path_info = os.path.join(log_path, f'{time.strftime("%Y-%m-%d")}_info.log')
log_path_warning = os.path.join(log_path, f'{time.strftime("%Y-%m-%d")}_warning.log')
log_path_error = os.path.join(log_path, f'{time.strftime("%Y-%m-%d")}_error.log')

# 日志简单配置 文件区分不同级别的日志
logger.add(log_path_info, rotation="00:00", retention='1 week', encoding='utf-8', enqueue=False, level='INFO')
# logger.add(log_path_warning, rotation="00:00", retention='1 week', encoding='utf-8', enqueue=True, level='WARNING')
logger.add(log_path_error, rotation="00:00", retention='1 week', encoding='utf-8', enqueue=False, level='ERROR')


__all__ = ["logger", "code_dir", "automation_log_dir", "automation_script_dir"]
