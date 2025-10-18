# -*- coding: utf-8 -*-

"""
descr: 基于pymysql封装mysql客户端
auther: lj.michale
create_date: 2025/9/27 15:54
file_name: mysql_client.py
"""

from dbutils.pooled_db import PooledDB
import pymysql
import logging
import traceback


class MysqlClient:
    """
    descr: Mysql多线程同步连接池
    """
    def __init__(self,
                 host,
                 database,
                 user=None,
                 password=None,
                 port=3306,
                 charset="utf8mb4",
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
            creator=pymysql,
            maxconnections=max_connections,
            mincached=min_cached,
            maxcached=max_cached,
            blocking=blocking,
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
            charset=charset,
            use_unicode=True,
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )

    def _get_conn(self):
        """
        获取conn连接
        :return:
        """
        return self._pool.connection()

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

    def get(self, sql, params=None):
        conn = self._get_conn()
        cursor = conn.cursor()
        try:
            cursor.execute(sql, params)
            return cursor.fetchone()
        finally:
            cursor.close()
            conn.close()

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

    def insert(self,
               sql,
               params=None):
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

    def table_has(self,
                  table_name,
                  field,
                  value):
        """
        是否存在某值
        :param table_name:
        :param field:
        :param value:
        :return:
        """
        sql = f"SELECT {field} FROM {table_name} WHERE {field}=%s LIMIT 1"
        return self.get(sql, value)

    def table_insert(self,
                     table_name,
                     item: dict):
        """
         表数据插入
        :param table_name:
        :param item:
        :return:
        """
        fields = list(item.keys())
        values = list(item.values())
        placeholders = ','.join(['%s'] * len(fields))
        field_list = ','.join(fields)
        sql = f"INSERT INTO {table_name} ({field_list}) VALUES ({placeholders})"
        try:
            return self.execute(sql, values)
        except pymysql.MySQLError as e:
            if e.args[0] == 1062:
                logging.warning("重复插入被跳过")
            else:
                logging.error("插入数据出错: %s\n数据: %s", e, item)
                raise

    def table_update(self,
                     table_name,
                     updates: dict,
                     field_where: str, value_where):
        """
        表更新
        :param table_name:
        :param updates:
        :param field_where:
        :param value_where:
        :return:
        """
        set_clause = ', '.join([f"{k}=%s" for k in updates])
        values = list(updates.values()) + [value_where]
        sql = f"UPDATE {table_name} SET {set_clause} WHERE {field_where}=%s"
        self.execute(sql, values)



