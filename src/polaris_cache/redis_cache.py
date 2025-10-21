# -*- coding: utf-8 -*-
"""
descr: 日期处理工具类
auther: lj.michale
create_date: 2025/9/19 17:11
file_name: date_time_utils.py
"""

import redis
from typing import Any

class RedisCache:
    def __init__(self,
                 host: str = 'localhost',
                 port: int = 6379,
                 db: int = 0,
                 password: str = None):
        """
        初始化Redis连接。
        :param host: Redis服务器地址
        :param port: Redis服务器端口
        :param db: Redis数据库编号
        :param password: Redis服务器密码
        """
        self.redis = redis.StrictRedis(host=host, port=port, db=db, password=password)

    def set(self, key: str, value: Any, ex: int = None) -> bool:
        """
        设置缓存。
        :param key: 缓存键
        :param value: 缓存值，可以是任何可序列化的Python对象
        :param ex: 过期时间（秒）
        :return: 设置成功返回True，否则返回False
        """
        try:
            self.redis.set(key, value, ex=ex)
            return True
        except redis.RedisError:
            return False

    def get(self, key: str) -> Any:
        """
        获取缓存。
        :param key: 缓存键
        :return: 缓存值，如果键不存在则返回None
        """
        return self.redis.get(key)

    def delete(self, key: str) -> bool:
        """
        删除缓存。
        :param key: 缓存键
        :return: 删除成功返回True，否则返回False
        """
        try:
            self.redis.delete(key)
            return True
        except redis.RedisError:
            return False

    def exists(self, key: str) -> bool:
        """
        检查键是否存在。
        :param key: 缓存键
        :return: 如果键存在返回True，否则返回False
        """
        return self.redis.exists(key)
