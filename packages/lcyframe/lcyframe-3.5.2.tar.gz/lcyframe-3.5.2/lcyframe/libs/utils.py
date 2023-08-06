# coding=utf-8
import logging
import hmac
import base64
import random
import time
from pathlib import Path
from datetime import timedelta, datetime, date
from string import ascii_letters
import zlib
import hashlib, string
import json
from bson.objectid import ObjectId
import operator
import re
import traceback

_chars = string.printable[:87] + '_' + string.printable[90:95]
to_ObjectId = lambda a: ObjectId(a) if type(a) != ObjectId else a
to_python = lambda s: json.loads(s)
to_json = lambda obj: json.dumps(obj, ensure_ascii=False, sort_keys=True)
fix_path = lambda path: Path(path).as_posix()
traceback = traceback

num_or_alpha = re.compile("^(?!\d+$)[\da-zA-Z_]{5,10}$")                            # 仅数字和字母组合，不允许纯数字,长度5~10
startwith_alpha = re.compile("^[a-zA-Z]{5,10}")                                     # 仅允许以字母开头,长度5~10
lllegal_char = re.compile('^[_a-zA-Z0-9\u4e00-\u9fa5]+$')                           # 仅允许中文、英文、数字,_下划线。但不允许非法字符
email_re = re.compile("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$")    # 是否是邮箱
phone_re = re.compile("^(0|86|17951)?(13|14|15|16|17|18)[0-9]{9}$")                 # 11位手机号
password_normal = re.compile("^(?:(?=.*)(?=.*[a-z])(?=.*[0-9])).{6,12}$")      # 一般密码 密码必须包含字母，数字,任意字符，长度6~12
password_strong = re.compile("^(?:(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])).{6,12}$")      # 强密码 密码必须包含大小写，数字,任意字符，长度6~12

def random_int(length=6):
    """生成随机的int 长度为length"""
    return ("%0" + str(length) + "d") % random.randint(int("1" + "0" * (length - 1)), int("9" * length))

def gen_random_str(length=6, chars=_chars):
    return ''.join(random.choice(chars) for i in range(length))

def gen_random_sint(length=6):
    """
    获取字符串加数字的随机值
    :param length:
    :return:
    """
    return "".join(random.choice(string.hexdigits) for i in range(length))

def random_string(length=6):
    """生成随机字符串"""
    return ''.join(random.choice(ascii_letters) for i in range(length))

def gen_hmac_key():
    """随机生成长度32位密文"""
    s = str(ObjectId())
    k = gen_random_str()
    key = hmac.HMAC(k, s).hexdigest()
    return key

def enbase64(s):
    """
    编码
    :param s:
    :return:
    """
    if type(s) == bytes:
        return base64.b64encode(s)
    else:
        s = s.encode('utf-8')
        return base64.b64encode(s).decode('utf-8')

def debase64(s):
    """
    解码
    :param s:
    :return:
    """
    bytes_types = (bytes, bytearray)
    return base64.b64decode(s) if isinstance(s, bytes_types) else base64.b64decode(s).decode()


class TypeConvert(object):
    """类型转换类, 处理参数"""
    MAP = {int: int,
           float: float,
           bool: bool,
           str: str}

    STR2TYPE = {"int": int,
                "integer": int,
                "string": str,
                "str": str,
                "bool": bool,
                "float": float,
                "list": list,
                "dict": dict,
                "json": json.loads}

    @classmethod
    def apply(cls, obj, raw):
        try:
            tp = type(obj)
            if tp in TypeConvert.MAP:
                return TypeConvert.MAP[tp](raw)
            return obj(raw)
        except Exception as e:
            logging.error("in TypeConvert.apply %s, obj: %s, raw: %s" % (e, obj, raw))
            return None

    @classmethod
    def convert_params(cls, _type, value):
        if _type in ["int", "integer"] and not value:
            value = 0
        try:
            tp = TypeConvert.STR2TYPE[_type]
            return tp(value)
        except Exception as e:
            raise e

def calculate_age(ts):
    """计算年龄"""
    if ts == -1:
        return -1
    born = datetime.fromtimestamp(ts)
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


def now():
    return int(time.time())

def oid_to_date(oid):
    return int_to_date_string(int(str(oid)[:8], 16))


def int_to_date_string(ts, fm=False):
    fm = fm if fm else "%Y-%m-%d %H:%M"
    try:
        if not ts:
            ts = 0
        return datetime.fromtimestamp(ts).strftime(fm)
    except:
        return datetime.fromtimestamp(time.time()).strftime(fm)

def str2timestamp(date_string, fm=False):
    fm = fm if fm else "%Y-%m-%d"
    return int(time.mktime(time.strptime(date_string, fm)))
    # return int(time.mktime(datetime.strptime(date_string, format).timetuple()))

def timestamp2str(ts, fm=False):
    return int_to_date_string(ts, fm)

def get_yesterday_midnight():
    # 获取昨天的午夜时间戳
    return get_today_midnight() - 86400

def get_today_midnight():
    # 获取今天的午夜时间戳
    now = int(time.time())
    return now - now % 86400 - 3600 * 8 - 86400

def get_today_lasttime():
    # 获取今天最后一秒时间戳
    now = int(time.time())
    return now - now % 86400 - 3600 * 8 + 24 * 3600 - 1


def get_delta_day(day=1):
    """
    获取n天后的时间
    :param day:
    :return:
    """

    now = datetime.now()

    # 当前日期
    now_day = now.strftime('%Y-%m-%d %H:%M:%S')

    # n天后
    delta_day = (now + timedelta(days=int(day))).strftime("%Y-%m-%d %H:%M:%S")
    return delta_day

def get_ts_from_object(s):
    if len(s) == 24:
        return int(s[:8], 16)
    return 0

def compress_obj(dict_obj, compress=True):
    """反序列化dict对象"""
    dict_obj = {"$_key_$": dict_obj} if not isinstance(dict_obj, dict) else dict_obj
    if compress:
        return zlib.compress(to_json(dict_obj))
    return to_json(dict_obj)

def uncompress_obj(binary_string, compress=True):
    """反序列化dict对象"""
    if compress:
         dict_obj = to_python(zlib.decompress(binary_string))
    else:
        dict_obj = to_python(binary_string)

    if "$_key_$" in dict_obj:
        return dict_obj["$_key_$"]
    else:
        return dict_obj

def get_mod(uid, mod=10):
    return int(uid) % mod

def gen_salt(len=6):
    return ''.join(random.sample(string.ascii_letters + string.digits, len))

def gen_salt_pwd(salt, pwd):
      return hashlib.md5((str(salt) + str(pwd)).encode("utf-8")).hexdigest()

def md5(s):
    return hashlib.md5(s).hexdigest()


def version_cmp(version1, version2):
    """比较系统版本号
    v1 > v2 1
    v1 = v2 0
    v1 < v2 -1
    v1: 用户使用的版本
    v2：最新上线的版本
    """

    def normalize(v):
        return [int(x) for x in re.sub(r'(\.0+)*$', '', v).split(".")]

    return operator.gt(normalize(version2), normalize(version1))

def _find_option_with_arg(argv, short_opts=None, long_opts=None):
    """Search argv for options specifying short and longopt alternatives.

    Returns:
        str: value for option found
    Raises:
        KeyError: if option not found.

    Example：
        config_name = _find_option_with_arg(short_opts="-F", long_opts="--config")
    """
    for i, arg in enumerate(argv):
        if arg.startswith('-'):
            if long_opts and arg.startswith('--'):
                name, sep, val = arg.partition('=')
                if name in long_opts:
                    return val if sep else argv[i + 1]
            if short_opts and arg in short_opts:
                return argv[i + 1]
    raise KeyError('|'.join(short_opts or [] + long_opts or []))

def check2json(data):
    if isinstance(data, (list, tuple)):
        for index, item in enumerate(data):
            data[index] = check2json(item)
        return data
    elif isinstance(data, dict):
        for key, value in data.items():
            data[key] = check2json(value)
        return data
    elif isinstance(data, ObjectId):
        return str(data)
    else:
        return data


def verify_username(username, min: int =4, max: int =10):
    """
    校验用户名
    :param username: 待验证用户名
    :param min: 最小长度
    :param max: 最大长度
    :return:
    """
    re_str1 = re.compile("^[a-zA-Z](?!\d+$)[\da-zA-Z_]")      # 非数字开头
    re_str2 = re.compile("^(?!\d+$)[\da-zA-Z_]{%d,%d}$" % (min, max))      # 非数字开头，字母与数字组合，长度4~10

    return re.search(re_str1, username) and re.search(re_str2, username)

def verify_nickname(nickname, min: int = 4, max: int = 10):
    """
    校验昵称
    :param nickname: 待验证昵称
    :param min: 最小长度
    :param max: 最大长度
    :return:
    """
    # 允许中文、字母、数字组合，禁止非法字符,长度4~10
    lllegal_char = re.compile('^[_a-zA-Z0-9\u4e00-\u9fa5]{%d,%d}$' % (min, max))
    return re.search(lllegal_char, nickname)

def verify_password(password, min: int = 4, max: int = 10, strong=True):
    """
    校验密码
    :param password: 待验证密码
    :param min: 最小长度
    :param max: 最大长度
    :param strong: true 强密码 false 一般密码

    :return:
    """
    password_normal = re.compile("^(?:(?=.*)(?=.*[a-z])(?=.*[0-9])).{%d,%d}$" % (min, max))  # 一般密码 密码必须包含字母，数字,任意字符，长度6~12
    password_strong = re.compile("^(?:(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])).{%d,%d}$" % (min, max))  # 强密码 密码必须包含大小写，数字,任意字符，长度6~12

    if strong:
        return re.search(password_strong, password)
    else:
        return re.search(password_normal, password)

def verify_phone(phone, min: int = 4, max: int = 10):
    """
    校验手机号
    :param phone: 待验证phone
    :param min: 最小长度
    :param max: 最大长度

    :return:
    """
    phone_re = re.compile("^(0|86|17951)?(13|14|15|16|17|18)[0-9]{9}$")                 # 11位手机号
    return re.search(phone_re, phone)

def verify_email(email, min: int = 4, max: int = 10):
    """
    校验邮箱
    :param phone: 待验证邮箱
    :param min: 最小长度
    :param max: 最大长度

    :return:
    """
    email_re = re.compile("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$")    # 是否是邮箱
    return re.search(email_re, email)

def verify_ip(ip, IPv6=True):
    """
    校验IP
    :param phone: 待验证ip
    :param min: 最小长度
    :param max: 最大长度

    :return:
    """
    ipv4_re = r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"    # IPV4
    ipv6_re = r"^(?:[A-F0-9]{1,4}:){7}[A-F0-9]{1,4}$"    # IPV6
    if IPv6:    # 大小写不敏感
        return re.search(ipv4_re, ip, re.I) or re.search(ipv6_re, ip)
    else:
        return re.search(ipv4_re, ip)

