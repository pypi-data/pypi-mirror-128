# coding:utf-8
# 一堆工具
import base64
import calendar
import datetime
import hashlib
import importlib
import io
import json
import logging
import os
import random
import re
import threading
import traceback
from collections import OrderedDict
from importlib import import_module as _import_module

import hashlib
import itertools
import json
import logging
import os
import random
import shutil
import string
import uuid
import warnings
import zipfile

from decimal import Decimal

import redis

import requests
from django.conf import settings
from django.core.cache import cache
from django.core.paginator import Paginator

from log_request_id import local

import time
from django.db import models
from django.db.models.query import QuerySet
from objectdict import ObjectDict as _ObjectDict
from rest_framework import serializers
from rest_framework.utils.encoders import JSONEncoder
import functools

try:
    from hashlib import sha1
except ImportError:
    from sha import sha as sha1

SortedDict = OrderedDict
ObjectDict = _ObjectDict

TIMEFORMAT = '%H:%M:%S'
DATEFORMAT = '%Y-%m-%d'
DATETIMEFORMAT = '%Y-%m-%d %H:%M:%S'
CONVERT_FORMAT = {"datetime": DATETIMEFORMAT, "date": DATEFORMAT, "time": TIMEFORMAT}


def find_djapp_name(app_root_path):
    for p in os.listdir(app_root_path):
        app_path = os.path.join(app_root_path, p)
        if os.path.isdir(app_path) and os.path.exists(os.path.join(app_path, '__init__.py')):
            yield p


class SingleInstance(object):
    _instance = None
    __instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        with cls.__instance_lock:
            if cls._instance is None:
                cls._instance = object.__new__(cls)
            return cls._instance

    @classmethod
    def get_instance(cls):  # type self
        return cls._instance


def sort_set_list(l):
    new_list = list(l)
    set_list = list(set(new_list))
    set_list.sort(key=new_list.index)
    return set_list


def watch_module_reload(the_module):
    module_path = the_module.__file__
    if module_path.endswith(".pyc") or module_path.endswith(".pyo"):
        module_path = module_path[:-1]
    the_file_module_st_mtime = os.stat(module_path).st_mtime
    the_module_last_mtime = getattr(the_module, 'module_st_mtime', 0)

    if the_module_last_mtime and the_file_module_st_mtime > the_module_last_mtime:
        try:
            logging.info('reload %s ' % the_module)
            importlib.reload(the_module)
            the_module_last_mtime = 0
        except Exception as e:
            logging.error('reload error %s,%s' % (the_module, e))
            traceback.print_exc()
    if the_module_last_mtime == 0:
        setattr(the_module, 'module_st_mtime', the_file_module_st_mtime)

    return the_module


def import_module(name):
    return _import_module(name)


def import_func(name):
    module, func = name.rsplit('.', 1)
    return getattr(import_module(module), func)


import_view = import_func
import_module_attr = import_view

import functools
from inspect import isfunction


class DecoratorsPartial(object):
    """
    语法糖使用装饰器能去掉括号()
    """

    def __init__(self, decorator_func, *args, **kwargs):
        self.decorator_func = decorator_func
        self.args = args
        self.kwargs = kwargs

    def __call__(self, *args, **kwargs):
        if len(args) == 1 and isfunction(args[0]):
            return self.decorator_func(*self.args, **self.kwargs)(args[0])
        else:
            @functools.wraps(self.decorator_func)
            def decorator(func):
                return self.decorator_func(*(args or self.args), **(kwargs or self.kwargs))(func)

            return decorator


class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime(DATETIMEFORMAT)
        return json.JSONEncoder.default(self, obj)


class MyJsonEncoder(JSONEncoder):
    def default(self, obj):

        if isinstance(obj, models.Model):
            if hasattr(obj, 'to_dict'):
                return obj.to_dict()
        elif isinstance(obj, QuerySet):
            return [m.to_dict() if hasattr(m, 'to_dict') else m for m in obj]
        elif isinstance(obj, serializers.Serializer):
            return obj.data
        if hasattr(obj, '__getstate__'):
            return obj.__getstate__()
        try:
            return super().default(obj)
        except TypeError as e:
            return str(obj)


def json_dumps(obj, *args, **kwargs):
    return json.dumps(obj, ensure_ascii=False, cls=MyJsonEncoder, *args, **kwargs)


def json_loadsobj(json_str, *args, **kwargs):
    return json.loads(json_str, object_hook=ObjectDict, *args, **kwargs)


def mkdirs(path, mode=0o755):
    if not os.path.exists(path):
        os.makedirs(path, mode)
    return path


def del_files(folder_path):
    for file_item in os.listdir(folder_path):
        try:
            itemsrc = os.path.join(folder_path, file_item)
            if os.path.isfile(itemsrc):
                os.remove(itemsrc)
        except Exception as e:
            logging.error(e)


def get_files_from_dir(dir_path, filter_endswith=''):
    for dirpath, dirs, files in os.walk(dir_path):
        for filename in files:
            if filename.endswith(filter_endswith):
                yield os.path.join(dirpath, filename)


def trace_msg():
    """跟踪消息
    """
    fp = io.StringIO()
    traceback.print_exc(file=fp)
    message = fp.getvalue()
    return message


def md5(s):
    sign_str = hashlib.md5()
    sign_str.update(s.encode('utf-8'))
    return sign_str.hexdigest()


def i2sl(num):
    """整形转36进制
    """
    loop = '0123456789abcdefghijklmnopqrstuvwxyz'
    n = num
    a = []
    while n != 0:
        a.append(loop[n % 36])
        n = n / 36
    a.reverse()
    return ''.join(a)


def str_to_datetime(datetime_str):
    return datetime.datetime.strptime(datetime_str, DATETIMEFORMAT)


def datetime_to_str(_datetime, format=DATETIMEFORMAT):
    """
    @_datetime 要转成字符串datetime对象
    """
    return _datetime.strftime(format)


def timestamp_to_datetime_str(timestamp, _format="datetime"):
    """
    @timestamp 时间戳转日期时间字符串
    @_format CONVERT_FORMAT
    """
    if _format not in list(CONVERT_FORMAT.keys()):
        return ""
    return datetime.datetime.fromtimestamp(timestamp).strftime(CONVERT_FORMAT[_format])


def datetime_to_timestamp(datetime_or_str):
    """
    @datetime_or_str datetime或者日期时间字符串转时间戳
    """
    if isinstance(datetime_or_str, str):
        datetime_or_str = str_to_datetime(datetime_or_str)
    return int(time.mktime(datetime_or_str.timetuple()))


datetime_or_str_to_timestamp = datetime_to_timestamp


def get_now_str():
    """获取现在时间字符串
    @
    """
    return datetime.datetime.now().strftime(DATETIMEFORMAT)


def get_today_str():
    """获取当天字符串
    @
    """
    return datetime.datetime.now().strftime(DATEFORMAT)


def get_timezone():
    """获取当前时区
    @
    """
    return -time.timezone / 3600


def add_months(dt, months):
    """月份增加
    """
    month = dt.month - 1 + months
    year = dt.year + month / 12
    month = month % 12 + 1
    day = min(dt.day, calendar.monthrange(year, month)[1])
    return dt.replace(year=year, month=month, day=day)


_DATE_REGEX = re.compile(
        r'(?P<year>\d{4})-(?P<month>\d{1,2})-(?P<day>\d{1,2})'
        r'(?: (?P<hour>\d{1,2}):(?P<minute>\d{1,2}):(?P<second>\d{1,2})'
        r'(?:\.(?P<microsecond>\d{1,6}))?)?')


def convert_to_datetime(input_value):
    """
    Converts the given object to a datetime object, if possible.
    If an actual datetime object is passed, it is returned unmodified.
    If the input is a string, it is parsed as a datetime.

    Date strings are accepted in three different forms: date only (Y-m-d),
    date with time (Y-m-d H:M:S) or with date+time with microseconds
    (Y-m-d H:M:S.micro).

    :rtype: datetime
    """
    from datetime import date, datetime
    if isinstance(input_value, datetime):
        return input_value
    elif isinstance(input_value, date):
        return datetime.fromordinal(input_value.toordinal())
    elif isinstance(input_value, str):
        m = _DATE_REGEX.match(input_value)
        if not m:
            raise ValueError('Invalid date string')
        values = [(k, int(v or 0)) for k, v in list(m.groupdict().items())]
        values = dict(values)
        return datetime(**values)
    raise TypeError('Unsupported input type: %s' % type(input_value))


def is_valid_datetime(str):
    '''判断是否是一个有效的日期字符串'''
    try:
        convert_to_datetime(str)
        return True
    except:
        return False


def sshaDigest(passphrase, salt=None):
    """
    Return the salted SHA for `passphrase` which is passed as bytes.
    """
    if salt is None:
        salt = ''
        for i in range(8):
            salt += chr(random.randint(0, 127))
        salt = salt.encode('ascii')

    s = sha1()
    s.update(passphrase)
    s.update(salt)
    encoded = base64.encodestring(s.digest() + salt).rstrip()
    crypt = b'{SSHA}' + encoded
    return crypt


def make_sign(_d, sign_key, is_return_sign_str=False):
    sign_list = []
    for k in sorted(_d):
        if k == 'sign':
            continue
        v = _d.get(k)
        if isinstance(v, list):
            v = v[0]
        if isinstance(v, str):
            v = v.encode('utf-8')
        sign_list.append('%s=%s' % (k, v))
    sign_str = ''.join(sign_list)
    sign_str = '%s%s' % (sign_str, sign_key)
    if is_return_sign_str:
        return md5(sign_str), sign_str
    else:
        return md5(sign_str)


def check_sign(_d, sign_key, sign=''):
    sign = _d.get('sign', '') or sign
    sign = sign[0] if isinstance(sign, list) else sign
    my_sign, sign_str = make_sign(_d, sign_key, is_return_sign_str=True)
    is_pass = my_sign == sign
    return is_pass


def profile_time(f, *args, **kwargs):
    import time
    s = time.time()
    r = f(*args, **kwargs)
    use_t = (time.time() - s)
    print('use time : %s' % use_t)
    return r, use_t


def read_1970_time(str_second, time_format='%Y-%m-%d %H:%M:%S') -> str:
    """
    1970 年至今的秒数转时间
    """
    import time
    time_array = time.localtime(float(str_second))
    return time.strftime(time_format, time_array)


def get_request_id():
    return getattr(local, 'request_id', uuid.uuid4().hex) or uuid.uuid4().hex


def random_string(length: int = 32, choice=string.ascii_letters + string.digits) -> str:
    return ''.join([random.SystemRandom().choice(choice) for _ in range(length)])


def safe_pagination(object_list, page_size=10, page_num=1, max_page_size=100000):
    """
    安全地分页
    :param object_list: type=list
    :param page_size: 每页返回多少个
    :param page_num: 需要第几页数据
    :return: total_count,num_pages,pageContents (总个数,总页数,当前页内容)
    """
    page_contents = []

    page_size = min(page_size, max_page_size)
    pagination = Paginator(object_list, page_size)

    num_pages = pagination.num_pages

    if page_num <= num_pages:
        page = pagination.page(page_num)
        page_contents = list(page.object_list)

    total_count = pagination.count

    return total_count, num_pages, page_contents


def limit_field_size(log_content, max_size=10000):
    """
    限制一下logger打到elk的长度, 剩下的就截断

    先默认固定长度最大去到10000
    """
    return str(log_content)[:max_size]


def md5_encrypt(content):
    """
    md5加密数据
    """

    return hashlib.md5(content.encode('utf-8')).hexdigest()


def flatten(iterable):
    """
    展开可迭代对象
    """
    return list(itertools.chain(*iterable))


def cent_2_yuan(price):
    """
    分变元

    4 -> 0.04
    :param price: 分
    """
    return f'{float(price / 100.0)}'


def yuan_2_cent(price):
    """
    元变分

    0.04 -> 4
    :param price: 元
    """
    return int(Decimal(str(price)) * 100)


def os_mkdir(dir_path):
    """
    尝试创建个文件目录
    :param dir_path:  '/app/temporary'
    """
    try:
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
    except Exception:
        pass


def is_contain_symbol(keyword):
    """
    判断一下是否有特殊字符
    """
    return bool(re.search(r"\W", keyword))


def clean_old_files(dir_path, days=7):
    """
    删除某个目录**天之前的文件
    :param dir_path:
    :param days: 多少天前的数据, 默认是7天
    """

    # 删除过期的, 删除最近7天的数据
    try:
        now = time.time()
        for file in os.listdir(dir_path):
            old_file_path = os.path.join(dir_path, file)
            if os.stat(old_file_path).st_mtime < now - days * 86400 and os.path.isfile(old_file_path):
                os.remove(old_file_path)
    except Exception:
        pass


def clean_files(file_path):
    try:
        if os.path.isdir(file_path):
            shutil.rmtree(file_path)
        else:
            os.remove(file_path)
    except Exception:
        pass


def make_zip(source_dir, output_filename):
    """
    压缩目录

    :return:
    """
    with zipfile.ZipFile(output_filename, 'w') as zipf:
        # pre_len = len(os.path.dirname(source_dir))
        pre_len = len(source_dir)
        for parent, dirnames, filenames in os.walk(source_dir):
            for filename in filenames:
                pathfile = os.path.join(parent, filename)
                arcname = pathfile[pre_len:].strip(os.path.sep)  # 相对路径
                zipf.write(pathfile, arcname, zipfile.ZIP_DEFLATED)


def panda_check_nan(value, default_value=''):
    """
    panda检查是否为空值

    很难受，panda读出来的值如果为空的话，变成了'nan',这里需要判断一下
    :param value: panda读取来的值
    :param default_value: 如果为空是，返回出来默认值
    :return:
    """

    return value if value != 'nan' else default_value


def save_dict_cache(cache_key, value, cache_time=30 * 60):
    """
    存储dict类型到redis
    """
    try:
        cache.set(cache_key, json.dumps(value, ensure_ascii=False), cache_time)
    except Exception:
        pass


def load_dict_cache(cache_key):
    """
    从redis获取dict类型对象
    """
    try:
        result = json.loads(cache.get(cache_key, {}))
    except Exception:
        result = {}

    return result


def delete_cache(cache_key):
    """
    从缓存中删除数据
    """
    try:
        cache.delete(cache_key)
    except Exception:
        pass


def get_client_ip(request):
    """
    获取请求的ip
    """
    ip = ''

    try:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
    except Exception:
        pass

    return ip


def copy_file(source_file_path, dest_file_path):
    """
    复制文件
    :param source_file_path: 源文件
    :param dest_file_path: 目标复制到哪儿
    """
    try:
        if not os.path.exists(dest_file_path):
            shutil.copy(source_file_path, dest_file_path)
    except Exception:
        pass


def get_client_ip(request=None):
    """"""
    ip = ''

    try:
        # 1. 从local读取
        ip = getattr(local, 'request_ip', '')
        if not ip:
            # 2. 从headers读取我们指定的头部,一般再do_requests会用到
            ip = request.META.get('HTTP_X_REQUEST_IP')
        if not ip:
            # 3. 从nginx转发那里获取
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0]
        if not ip:
            # 4. 可能从cdn那里获取ip
            ip = request.META.get('HTTP_X_REQUEST_IP')
        if not ip:
            # 5. 最后没办法就从默认那里拿
            ip = request.META.get('REMOTE_ADDR')
    except Exception:
        pass

    return ip


def list2tree(obj_list, pk_key='id', parent_key='parent', children_key='children', allow_parent_null_add2root=True):
    """
     列表转树结构
    @param obj_list: 对象列表
    @param pk_key: 主键字段名
    @param parent_key: 父字段名
    @param children_key: 孩子字段名
    @param allow_parent_null_add2root: 找不到父节点 是否 添加到根
    @return: List
    """
    obj_map = {}
    tree_list = []
    for obj in obj_list:

        setattr(obj, children_key, [])
        pk = getattr(obj, pk_key, None)
        if pk:
            obj_map[pk] = obj

    for obj in obj_list:
        parent_pk = getattr(obj, parent_key, None)
        if parent_pk:
            # parent 是同类则从属性中获取 pk
            if isinstance(parent_pk, type(obj)):
                parent_pk = getattr(parent_pk, pk_key)
            parent_obj = obj_map.get(parent_pk, None)
            if parent_obj:
                getattr(parent_obj, children_key).append(obj)
                continue
        # 找不到父节点 是否 添加到根
        if allow_parent_null_add2root:
            tree_list.append(obj)
    return tree_list


if __name__ == '__main__':
    test_d = {'openId': ['4095339'], 'code': ['1'], 'userType': ['55'], 'timestamp': ['1446705211'],
              'sign'  : ['a0778e8de9e11aab411d89c22137b12c'], 'serverSign': ['2bed14fe0d68d1cefad6827bc11669e5'],
              'other' : [''], 'action': ['login'], 'message': [''], 'data': [
                    '{"timestamp":"1446705209","sign":"37e7b86faacdd55b7cff5361a611ac92","gameSimpleName":"fytx_test","other":"","c1":"a","sdkSimpleName":"i9133","c2":"a","sdkVersionCode":"V1_0","userType":"55","openId":"4095339"}']}
    key = 'asdb'
    sign = make_sign(test_d, key)
    test_d['sign'] = sign
    print(test_d)
    print(sign)
    print((check_sign(test_d, key)))
