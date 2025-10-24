# -*- coding: utf-8 -*-

"""
descr: 通用工具类
auther: lj.michale
create_date: 2025/9/27 15:54
file_name: common_utils.py
"""
import uuid
import time
import secrets
import string
import random

class CommonUtils:

    def create_random_0_1_number(self):
        """
        随机返回一个0-1之间的浮点数
        :return:
        """
        return random.random()

    def create_string_number(self,n):
        """
        生成一串指定位数的字符+数组混合的字符串
        :return:
        """
        m = random.randint(1, n)
        a = "".join([str(random.randint(0, 9)) for _ in range(m)])
        b = "".join([random.choice(string.ascii_letters) for _ in range(n - m)])
        return ''.join(random.sample(list(a + b), n))

    @staticmethod
    def generate_unique_id(length=10):
        # 定义要添加的字符集，包括大小写字母和数字
        characters = string.ascii_letters + string.digits
        # 使用secrets.choice来生成更安全的随机字符
        secure_id = ''.join(secrets.choice(characters) for _ in range(length))

        return secure_id

    @staticmethod
    def get_dict_key_value(dict):
        """
        获取字典所有key,value
        :param dict:
        :return:
        """
        keys = dict.keys()
        values = dict.values()
        return keys, values

    @staticmethod
    def get_uuid(params: dict):
        """
        基于名字的MD5散列值，同一命名空间的同一名字生成相同的uuid
        :param params:
        :return:
        """
        p1 = sorted(params.items(), key=lambda x: x[0])
        p2 = [str(p) for p in p1]
        p3 = '|'.join(p2)
        return str(uuid.uuid3(uuid.NAMESPACE_OID, p3))

    @staticmethod
    def time_cost(fn):
        """
        这个装饰器用于统计函数运行耗时
        :param fn:
        :return:
        """
        def _timer(*args, **kwargs):
            func_name = fn.__name__
            # LogUtil.info('start', func_name)
            start = time.perf_counter()
            result = fn(*args, **kwargs)
            end = time.perf_counter()
            cost = _fmt(end - start)
            # LogUtil.info('end', func_name)
            # LogUtil.info('cost', cost)
            return result

        def _fmt(sec):
            """格式化打印时间，大于60秒打印分钟，大于60分钟打印小时"""
            return f'{round(sec, 2)}s' if sec <= 60 else f'{round(sec / 60, 2)}m' if sec <= 3600 else f'{round(sec / 3600, 2)}h'

        return _timer


