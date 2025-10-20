# -*- coding: utf-8 -*-

"""
descr: 基于impyla,dbutils封装Oracle客户端
auther: lj.michale
create_date: 2025/9/27 15:54
file_name: impala_client.py
"""

from impala.dbapi import connect
from dbutils.pooled_db import PooledDB
import logging
import traceback


class OracleClient:
    def __init__(self,
                 host,
                 database,
                 user=None,
                 password=None,
                 port=21050,
                 max_connections=10,
                 min_cached=2, max_cached=5, blocking=True):
        """
        初始化连接池
        :param host:
        :param database:
        :param user:
        :param password:
        :param port:
        :param charset:
        :param max_connections:
        :param min_cached:
        :param max_cached:
        :param blocking:
        """
        self._pool = PooledDB(
            creator=connect,
            maxconnections=max_connections,
            mincached=min_cached,
            maxcached=max_cached,
            blocking=blocking,
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
        )

    def _get_conn(self):
        """
        获取conn连接
        :return:
        """
        return self._pool.connection()

    def execute(self,
                sql,
                params=None):
        """
        带参执行sql查询
        :param sql:
        :param params:
        :return:
        """
        conn = self._get_conn()
        cursor = conn.cursor()
        try:
            return cursor.execute(sql, params)
        except Exception as e:
            traceback.print_exc()
            logging.error(f"SQL执行错误: {e}\nSQL: {sql}\nParams: {params}")
            raise
        finally:
            cursor.close()
            conn.close()

    def insert(self,sql,params=None):
        """
        带参数插入
        :param sql:
        :param params:
        :return:
        """
        conn = self._get_conn()
        cursor = conn.cursor()
        try:
            cursor.execute(sql, params)
            return cursor.lastrowid
        except Exception as e:
            logging.error(f"插入出错: {e}\nSQL: {sql}\nParams: {params}")
            raise
        finally:
            cursor.close()
            conn.close()

    def query(self, sql, params=None):
        """
        sql查询
        :param sql:
        :param params:
        :return:
        """
        conn = self._get_conn()
        cursor = conn.cursor()
        try:
            cursor.execute(sql, params)
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()


if __name__ == '__main__':
    pool = OracleClient(
        host='10.53.0.71',
        database='impala',
        user='root',
        password='',
        port=21050
    )
    data_list = pool.query("select * from bi_ods.dw_quality_check_rules ")
    for data in data_list:
        print(data)
