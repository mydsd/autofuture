"""
Built-in functions used in YAML/JSON testcases.
"""

import datetime
import random
import string
import time
import hashlib
# from httprunner.compat import builtin_str, integer_types
# from httprunner.exceptions import ParamsError


def gen_random_string(str_len):
    """ generate random string with specified length
    """
    return ''.join(
        random.choice(string.ascii_letters + string.digits) for _ in range(str_len))


# def get_timestamp(str_len=13):
#     """ get timestamp string, length can only between 0 and 16
#     """
#     if isinstance(str_len, integer_types) and 0 < str_len < 17:
#         return builtin_str(time.time()).replace(".", "")[:str_len]
#
#     raise ParamsError("timestamp length can only between 0 and 16.")
def gen_token(sys_time,key):
    app_key = "96c0dd548137fceab40d776a8ddb9319"
    str_code = app_key + str(sys_time)+str(key)
    m = hashlib.md5()
    str_encode = str_code.encode(encoding='utf-8')
    m.update(str_encode)
    token = m.hexdigest()
    print(token)
    return token

def get_current_date(fmt="%Y-%m-%d"):
    """ get current date, default format is %Y-%m-%d
    """
    return datetime.datetime.now().strftime(fmt)


def sleep(n_secs):
    """ sleep n seconds
    """
    time.sleep(n_secs)

def add(a,b,c):
    return a+b+c