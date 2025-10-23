# -*- coding: utf-8 -*-

"""
descr: Redis客户端
auther: lj.michale
create_date: 2025/9/27 15:54
file_name: redis_client.py
"""
import logging
from polaris_common import CommonUtils
import redis

class RedisClient:
    """redis操作工具类
       conf = {
           'host': '',
           'port': '',
           'password': '',
           'db': '30000',
           'decode_responses': True,
       }
       """
    CONN = None
    CFID = None

    @classmethod
    def _init(cls, conf: dict):
        if cls.CONN is None:
            cls.connect(conf)
        elif cls.CFID != CommonUtils.get_uuid(conf):
            cls.connect(conf)

    @classmethod
    def connect(cls, conf: dict):
        try:
            pool = redis.ConnectionPool(**conf)
            cls.CONN = redis.Redis(connection_pool=pool)
            cls.CFID = CommonUtils.get_uuid(conf)
        except Exception as e:
            logging.error("redis init failed, please check the config", e)

    @classmethod
    def exist(cls, key: str):
        """
        判断key是否存在
        :param key:
        :return:
        """
        return cls.CONN.exists(key)

    @classmethod
    def get(cls, key: str):
        """
        字符串获取值
        :param key:
        :return:
        """
        return cls.CONN.get(key)

    @classmethod
    def set(cls, key: str, val: str):
        """
        字符串设置值
        :param key:
        :param val:
        :return:
        """
        cls.CONN.set(key, val)

    @classmethod
    def lget(cls, key: str):
        """
        列表获取值
        :param key:
        :return:
        """
        cls.CONN.lrange(key, 0, -1)

    @classmethod
    def lset(cls, key: dict, vals: tuple):
        """
        列表设置值
        :param key:
        :param vals:
        :return:
        """
        cls.CONN.lpush(key, vals)
