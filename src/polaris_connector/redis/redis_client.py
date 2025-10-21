# -*- coding: utf-8 -*-

"""
descr: Redis客户端
auther: lj.michale
create_date: 2025/9/27 15:54
file_name: redis_client.py
"""
import redis
from redis.connection import ConnectionPool

import redis

class RedisClient:
    def __init__(self, host='localhost', port=6379, db=0):
        self.client = redis.StrictRedis(host=host, port=port, db=db, decode_responses=True)

    def set(self, key, value):
        """
        设置键值对
        :param key:
        :param value:
        :return:
        """
        self.client.set(key, value)

    def get(self, key):
        """
        获取键的值
        :param key:
        :return:
        """
        return self.client.get(key)

    def delete(self, key):
        """
        删除键
        :param key:
        :return:
        """
        return self.client.delete(key)

    def exists(self, key):
        """
        检查键是否存在
        :param key:
        :return:
        """
        return self.client.exists(key)

    def hset(self, name, key, value):
        """
        设置哈希值
        :param name:
        :param key:
        :param value:
        :return:
        """
        self.client.hset(name, key, value)

    def hget(self, name, key):
        """
        获取哈希值
        :param name:
        :param key:
        :return:
        """
        return self.client.hget(name, key)

    def hgetall(self, name):
        """
        获取整个哈希表
        :param name:
        :return:
        """
        return self.client.hgetall(name)

