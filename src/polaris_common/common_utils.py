# -*- coding: utf-8 -*-

"""
descr: 通用工具类
auther: lj.michale
create_date: 2025/9/27 15:54
file_name: common_utils.py
"""
import os
import uuid
import time
import secrets
import string
import random
import hashlib

class CommonUtils:

    def create_random_int_number(self,n,m):
        """
        随机返回从n-m之间的整数
        :param n:
        :param m:
        :return:
        """
        return random.randint(n, m)

    def create_random_n_m_number(self,n,m):
        """
        随机返回一个n-m之间的浮点数
        :return:
        """
        return random.uniform(n, m)

    def create_string_number(self,n):
        """
        生成一串指定位数的字符+数组混合的字符串
        :return:
        """
        m = random.randint(1, n)
        a = "".join([str(random.randint(0, 9)) for _ in range(m)])
        b = "".join([random.choice(string.ascii_letters) for _ in range(n - m)])
        return ''.join(random.sample(list(a + b), n))

    def generate_ids(length, data_size, ration):
        """
        定义生成可重复ID的函数，其中参数ration为重复的ID占比，比如0.3
        :param length: 生成字符串长度
        :param data_size:
        :param ration:
        :return:
        """
        num_dupl = int(data_size*ration)
        ids = [str(CommonUtils.generate_unique_id(length)) for _ in range(data_size - num_dupl)]
        ids.extend(random.sample(ids, num_dupl))
        random.shuffle(ids)

        return ids

    @staticmethod
    def generate_unique_id(length=10):
        timestamp = str(int(time.time() * 1000))  # 使用毫秒级时间戳
        random_part = os.urandom(8).hex()  # 生成一个随机的16进制字符串作为随机部分
        combined = timestamp + random_part  # 组合时间戳和随机部分
        hashed = hashlib.sha256(combined.encode()).hexdigest()  # 使用SHA-256哈希算法进行哈希处理
        return hashed[:15]  # 取哈希值的前15位字符作为ID

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


if __name__ == '__main__':
    print(CommonUtils.generate_unique_id(15))