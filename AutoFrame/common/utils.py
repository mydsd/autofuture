import configparser
import re
from datetime import datetime
from datetime import timedelta
from datetime import date
import json,oss2
import os, subprocess
import time, requests, uuid
import urllib
import urllib.request
import uuid
# from locale import *
from typing import Generator
from common.logger import logger
import pdfkit
import pinyin
import builtins, shutil

from hashlib import md5
from engine.session import SessionLocal
from engine import load_conf
from apscheduler.triggers.cron import CronTrigger
# import urllib.request

# ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def read_ini(path):
    print(path)
    config = configparser.ConfigParser()
    config.read(path,encoding='utf-8')
    return config

def get_db() -> Generator:
    """
    获取sqlalchemy会话对象
    :return:
    """
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


# 获取当前时间
def get_time():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


# str格式时间转换成时间戳
def time_to_timestamp(times):
    time_array = time.strptime(times, "%Y-%m-%d %H:%M:%S")
    time_stamp = int(time.mktime(time_array))
    return time_stamp


# datetime格式时间转换成时间戳
def datetime_to_timestamp(times: datetime):
    time_stamp = int(time.mktime(times.timetuple()))
    return time_stamp

def get_datetime_now() -> datetime:
    """获取当前时间 datetime格式

    Returns:
        [type]: [description]
    """
    return datetime.now()

def get_delta_times(s_time: datetime, e_time: datetime) -> int:
    """获取时间差

    Args:
        s_time (datetime): 开始时间
        e_time (datetime): 结束时间

    Returns:
        int: 时间差的秒数
    """
    return int(e_time.timestamp()) - int(s_time.timestamp())


# 读取文件内容
def read_txt(path):
    with open(path, 'r') as f:
        data = f.read()
        return data


# 生成uuid
def gen_uuid() -> str:
    return uuid.uuid4().hex


# 读取ini配置文件
def get_conf(section, key):
    base_path = os.path.dirname(os.path.dirname((os.path.abspath(__file__))))
    conf_path = os.path.join(base_path, "conf.ini")

    conf = configparser.ConfigParser()
    conf.read(conf_path, "utf8")
    return conf.get(section, key)


def str2hump(src: str, first_upper: bool = False):
    """
    将下划线分隔的名字,转换为驼峰模式
    :param src: 要转换的字符串
    :param first_upper: 转换后的首字母是否指定大写(  testName or  TestName)
    :return:转换后的驼峰字符串
    """
    arr = src.split('_')
    res = ''
    for i in arr:
        res = res + i[0].upper() + i[1:]

    if not first_upper:
        res = res[0].lower() + res[1:]
    return res


# 对象集合转dict json
def to_dict_json(all_vendors):
    dict_json = [item.to_dict() for item in all_vendors]
    return dict_json


# 对象集合hump json
def to_hump_json(all_vendors):
    hump_json = [item.to_hump_dict() for item in all_vendors]
    return hump_json


# 保存网页为HTML格式文件
def url_to_html(url, file_path):
    # 查询目录是否存在，不存在则创建
    if not os.path.isdir(file_path):
        os.makedirs(file_path)

    html_page = urllib.request.urlopen(url).read()
    file_name = get_time() + '.html'
    file = file_path + '/' + file_name

    with open(file, 'wb') as f:
        f.write(html_page)

    return file.strip('.')  # 去除两边的.符号
# 保存网页为HTML格式文件
def cp_html(html_file, dest_dir):
    """复制html文件到目标目录

    Args:
        html_file ([type]): [description]
        dest_dir ([type]): [description]

    Returns:
        [type]: [description]
    """
    if not os.path.isdir(dest_dir):
        os.makedirs(dest_dir)

    # file_name = get_time() + '.html'
    # file = dest_dir + '/' + file_name
    file_name = f'{time.time()}.html'
    file = os.path.join(dest_dir, file_name)
    with open(file, 'w+') as fw:
        with open(html_file, 'r+') as fr:
            fw.write(fr.read())
    # os.system(f'cp {html_file} {file}')
    return file_name


# 保存网页为PDF文件
def url_to_pdf(url, path, file_path):
    # 查询目录是否存在，不存在则创建
    if not os.path.isdir(file_path):
        os.makedirs(file_path)

    # 设置wkhtmltopdf程序路径
    config = pdfkit.configuration(wkhtmltopdf=path)

    file_name = get_time() + '.pdf'
    file = file_path + '/' + file_name
    # 生成pdf文件
    pdfkit.from_url(url, file, configuration=config)

    return file.strip('.')  # 去除两边的.符号

def html_to_pdf(html_file: str, wk_path: str, pdf_dir: str):
    """将html文件转pdf

    Args:
        html_file (str): html文件路径
        wk_path (str): wkhtmltopdf程序路径
        pdf_dir (str): 目标pdf文件目录

    Returns:
        [type]: [description]
    """
    # 查询目录是否存在，不存在则创建
    if not os.path.isdir(pdf_dir):
        os.makedirs(pdf_dir)

    # 设置wkhtmltopdf程序路径
    config = pdfkit.configuration(wkhtmltopdf=wk_path)

    # file_name = get_time() + '.pdf'
    file_name = f'{time.time()}.pdf'
    file = os.path.join(pdf_dir, file_name)
    # 生成pdf文件
    pdfkit.from_file(html_file, file, configuration=config)

    return file_name  # 去除两边的.符号


# 千分位字符去除千分符
def num_change(num:str):
    # setlocale(LC_NUMERIC, 'zh_CN')
    # return atof(num)  # 2,746.12->2746.12
    s = ''.join(num.split(','))
    return float(s)


# 数据百分比(四舍五入取整)
def num_cov(num1, num2):
    if num2 != 0:
        cov = round(num1 / num2 * 100)
    else:
        cov = 0
    cov_string = str(cov) + '%'
    return cov_string


# 百分比字符串转换成数字
def cov_str_to_num(num):
    return round(float(num[:-1]))


# 驼峰转下划线
def get_lower_case_name(text):
    lst = []
    for index, char in enumerate(text):
        if char.isupper() and index != 0:
            lst.append("_")
        lst.append(char)
    return "".join(lst).lower()


# dict转小驼峰
def dict_lower_case_name(obj_in):
    return {get_lower_case_name(k): v for k, v in obj_in}

# dict键转小驼峰
def dict_key_lower_case_name(obj_in:dict):
    """将字典的键以小驼峰转换命名

    Args:
        obj_in (dict): 需转换的字典数据

    Returns:
        转换后的数据
    """
    return {get_lower_case_name(k): v for k, v in obj_in.items()}

# 获取首拼
def get_str_alphabet(value: str) -> str:
    return pinyin.get_initial(value, delimiter="").upper()


# 获取2个字符中间的字符串
def get_str_btw(s, f, b):
    """
    param s: 目标字符串
    param f: 开始字符
    param b：结尾字符
    """
    par = s.partition(f)
    return (par[2].partition(b))[0][:].strip()


def get_date_list(days):
    """返回前days天日期列表"""
    date_list = list()
    for i in range(0, days + 1):
        day = datetime.now() - timedelta(days=i)
        date_to = datetime(day.year, day.month, day.day)
        date_list.append(date_to.strftime("%Y-%m-%d"))
    return date_list


def upload_file_to_oss(file_name, file_content):
    """
    上传文件到oss
    :param file_name: 上传后的文件名
    :param file_content: 上传的源文件
    :return:
    """

    auth = oss2.Auth(load_conf.access_key, load_conf.access_secret)
    bucket = oss2.Bucket(auth, load_conf.endpoint, load_conf.bucket_name, connect_timeout=30)

    res = bucket.put_object(file_name, file_content)
    if res.status == 200:
        # 上传成功，获取文件带签名的地址，返回给前端，失效时间10年
        expire = 3600*24*365*10
        url = bucket.sign_url('GET', file_name, expire)
        return {"url": url}
    else:
        return None


class Dict(dict):
    __setattr__ = dict.__setitem__
    __getattr__ = dict.__getitem__


def dict_to_object(dictObj):
    """
    将字典转成对象
    :param dictObj:
    :return:
    """
    if not isinstance(dictObj, dict):
        return dictObj
    inst = Dict()
    for k, v in dictObj.items():
        inst[k] = dict_to_object(v)
    return inst


# def subprocess_cmd(cmd: str, timeout: int=0, cwd: str=None, log_file: str=None, stdout=subprocess.PIPE, stderr=subprocess.STDOUT):
#     logger.debug(f'开始执行shell命令 {cmd}')
#     try:
#         sub = subprocess.run(cmd, shell=True, timeout=timeout, cwd=cwd, stdout=stdout, stderr=stderr, encoding="utf-8")
#     except subprocess.TimeoutExpired as e:
#         logger.exception(f'执行{cmd}超时 {e}')
#         return
#     if sub.returncode != 0:
#         logger.error('执行{cmd}异常')
#         return
#     if log_file:
#         with open(log_file, 'a+', encoding='utf-8') as fw:
#             for line in sub.stdout:
#                 fw.write(line)
#     return True

def parse_url(url: str, params: dict=None, header: dict=None, timeout: int=5, times: int=3):
    """发起get请求并解析

    Args:
        url (str): 请求URL
        params (dict, optional): 请求参数. Defaults to None.
        header (dict, optional): 请求header. Defaults to None.
        timeout (int, optional): 请求超时时间 秒. Defaults to 5.
        times (int, optional): 重试次数. Defaults to 3.

    Returns:
        [dict]: 响应json
    """
    current_times = 1
    while current_times < times:
        try:
            resp = requests.get(url, params=params, headers=header, timeout=timeout)
            if resp.status_code == 200:
                return resp.json()
            logger.warning(f'请求{url}失败，重试{current_times}')
        except Exception as e:
            logger.exception(f'发生请求异常 {url} 重试{current_times} {e}')
        current_times += 1


def to_json_func(all_vendors):
    """
    使用sql语句直接查询后(查询部分字段)，把查询结果转为字典列表[{},{},{}]
    :param all_vendors:
    :return:
    """
    v = [to_dict_func(ven) for ven in all_vendors]
    return v


def to_dict_func(self):
    result = {}
    for key in self._parent.keys:
        if getattr(self, key) is not None:
            result[key] = builtins.str(getattr(self, key))
        else:
            result[key] = getattr(self, key)
    return result


def class_to_dict(obj):
    '''把对象(支持单个对象、list、set)转换成字典'''
    is_list = obj.__class__ == [].__class__
    is_set = obj.__class__ == set().__class__

    if is_list or is_set:
        obj_arr = []
        for o in obj:
            # 把Object对象转换成Dict对象
            dict = {}
            dict.update(o.__dict__)
            obj_arr.append(dict)
        return obj_arr
    else:
        dict = {}
        dict.update(obj.__dict__)
        return dict

def crontab_check(s: str):
    """cron表达式验证

    Args:
        s (str): 表达式字符串

    Returns:
        [type]: [description]
    """
    try:
        trigger =CronTrigger.from_crontab(s)
    except Exception as e:
        logger.exception(f'cron表达式错误, {e}')
        return
    return trigger

def get_md5(s: str):
    return md5(bytes(s, encoding='utf-8')).hexdigest()


def interval_time(date):
    """获取当前时间距离指定时相差的秒值
    :param date: 格式为："2021-07-28 18:25:30"
    :return: 返回秒
    """
    now_time = int(time.time())
    # 触发时间精确到分
    trigger_time = int(time.mktime(time.strptime(date, "%Y-%m-%d %H:%M:%S")))
    if trigger_time > now_time:
        seconds = trigger_time - now_time
    else:
        seconds = now_time - trigger_time
    return seconds

def get_jarName(args):
    jarName = []
    for i in args:
        if ".jar" in i:
            jarName.append(i)
    return jarName

def download_file_from_oss(remoteFile,localFile):
    auth = oss2.Auth(load_conf.access_key, load_conf.access_secret)
    bucket = oss2.Bucket(auth, load_conf.endpoint, load_conf.bucket_name, connect_timeout=30)

    res = bucket.get_object_to_file(remoteFile,localFile)
    return res.status

def rm_file_from_oss(remoteFile):
    auth = oss2.Auth(load_conf.access_key, load_conf.access_secret)
    bucket = oss2.Bucket(auth, load_conf.endpoint, load_conf.bucket_name, connect_timeout=30)
    res = bucket.delete_object(remoteFile)
    return res.status


def write_data(filename: str, data: str):
    """
    写json文档
    """
    with open(os.path.join(filename + '.json'), 'w', encoding='utf-8') as f:
        f.write(data)


def read_data(filename: str):
    """
    读取json类型文档
    Args:
        filename (str): 文件名

    Returns:
        转换后的数据
    """
    data_dict = {}
    with open(os.path.join(filename + '.json'), 'r', encoding='utf-8') as f:
        result = f.read()
        data_list = json.loads(result)
        data_dict[filename] = data_list
        return data_list
def check_clear_file(d: str, las: int=0):
    """删除指定目录下的指定时间前的文件

    Args:
        d (str): [目标目录]
        las (int, optional): [多少秒前]. Defaults to 0.
    """
    for i in os.listdir(d):
        if las and os.path.getctime(f'{d}/{i}') > (time.time() - las):
            continue
        shutil.rmtree(f'{d}/{i}')

def get_uuid(s):
    """ 生成uuid

    Args:
        s (str): [description]

    Returns:
        [type]: [description]
    """
    return uuid.uuid5(uuid.NAMESPACE_OID, s).hex


def get_nday_list(n):
    """
    获取当天之前的日期列表(包含当天)
    :param n:
    :return:
    """
    before_n_days = []
    for i in range(0, n)[::-1]:
        before_n_days.append(str(date.today() - timedelta(days=i)))
    return before_n_days

def cname(s):
    s = re.sub(r"(\s|_|-)+"," ",s).title().replace(' ','')
    return s[0].lower()+s[1:]

def batch_hump(slist):
    if isinstance(slist,list):
        hump =[]
        for s in slist:
            tmp = {}
            for k,v in s.items():
                tmp[cname(k)] = v
            hump.append(tmp)
        return hump
    else:
        return slist