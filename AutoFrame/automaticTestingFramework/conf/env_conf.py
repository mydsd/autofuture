import os
import datetime

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 测试host
# TEST_HOST = 'http://yuxi-dev.seenew.info:81'
TEST_HOST = 'http://127.0.0.1:8081'

# 测试数据路径
#CASE_DATA_PATH = os.path.join(BASE_PATH, 'data', 'test_cases.xlsx')
Token_DATA_PATH = os.path.join(BASE_PATH, 'data', 'token.json')
GLOBAL_DATA_PATH = os.path.join(BASE_PATH, 'data', 'global_vars.json')
HEADER_DATA_PATH = os.path.join(BASE_PATH, 'data', 'header.json')

# 自定义脚本路径
SCRIPT_PATH = os.path.join(BASE_PATH, 'scripts')

# 报告生成的路径
REPORT_SAVED_PATH = os.path.join(BASE_PATH, 'report', 'api_')
REPORT_NEWEST_PATH = os.path.join(BASE_PATH, 'report', 'newest', 'report.html')
MAIL_REPORT_PATH = os.path.join(BASE_PATH, 'report', 'email', 'api_')
MAIL_IMG_PATH = os.path.join(BASE_PATH, 'report', 'email', 'img', 'api_')

# 报告模板路径
REPORT_TEMPLATE_PATH = os.path.join(BASE_PATH, 'report', 'template', 'detail_report.html')
MAIL_TEMPLATE_PATH = os.path.join(BASE_PATH, 'report', 'template', 'mail_report.html')

# ---------------- 日志相关 --------------------
# 日志级别
LOG_LEVEL = 'debug'
LOG_STREAM_LEVEL = 'debug'  # 屏幕输出流
LOG_FILE_LEVEL = 'info'  # 文件输出流

# 日志文件命名
LOG_FILE_NAME = os.path.join(BASE_PATH, 'logs', datetime.datetime.now().strftime('%Y-%m-%d') + '.log')

if __name__ == '__main__':
    print(LOG_FILE_NAME)