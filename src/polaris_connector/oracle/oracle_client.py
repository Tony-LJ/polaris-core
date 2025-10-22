# -*- coding: utf-8 -*-

"""
descr: 基于oracledb,dbutils封装Oracle客户端
       dsn=host:port/service_name
auther: lj.michale
create_date: 2025/9/27 15:54
file_name: oracle_client.py
"""
import oracledb
from dbutils.pooled_db import PooledDB
import logging
import traceback
from oracledb import connect


# class OracleClient:
#     def __init__(self,
#                  dsn,
#                  user=None,
#                  password=None,
#                  port=1521,
#                  max_connections=10,min_cached=2, max_cached=5, blocking=True):
#         """
#         初始化连接池
#         :param host:
#         :param db:
#         :param user:
#         :param password:
#         :param port:
#         :param charset:
#         :param max_connections:
#         :param min_cached:
#         :param max_cached:
#         :param blocking:
#         """
#         self._pool = PooledDB(
#             creator=connect,
#             maxconnections=max_connections,
#             mincached=min_cached,
#             maxcached=max_cached,
#             blocking=blocking,
#             host=host,
#             port=port,
#             user=user,
#             password=password,
#             db=db
#         )
#
#     def _get_conn(self):
#         """
#         获取conn连接
#         :return:
#         """
#         return self._pool.connection()
#
#     def execute(self,
#                 sql,
#                 params=None):
#         """
#         带参执行sql查询
#         :param sql:
#         :param params:
#         :return:
#         """
#         conn = self._get_conn()
#         cursor = conn.cursor()
#         try:
#             return cursor.execute(sql, params)
#         except Exception as e:
#             traceback.print_exc()
#             logging.error(f"SQL执行错误: {e}\nSQL: {sql}\nParams: {params}")
#             raise
#         finally:
#             cursor.close()
#             conn.close()
#
#     def insert(self,sql,params=None):
#         """
#         带参数插入
#         :param sql:
#         :param params:
#         :return:
#         """
#         conn = self._get_conn()
#         cursor = conn.cursor()
#         try:
#             cursor.execute(sql, params)
#             return cursor.lastrowid
#         except Exception as e:
#             logging.error(f"插入出错: {e}\nSQL: {sql}\nParams: {params}")
#             raise
#         finally:
#             cursor.close()
#             conn.close()
#
#     def query(self, sql, params=None):
#         """
#         sql查询
#         :param sql:
#         :param params:
#         :return:
#         """
#         conn = self._get_conn()
#         cursor = conn.cursor()
#         try:
#             cursor.execute(sql, params)
#             return cursor.fetchall()
#         finally:
#             cursor.close()
#             conn.close()


if __name__ == '__main__':
    with oracledb.connect(user='hadoop', password='vSWnGLcdd8ch', dsn = 'ebsdb-scan.kinwong.com:1531/prod') as connection:
        with connection.cursor() as cursor:
            sql = """select * from ont.oe_order_lines_all where rownum <= 10"""
            for r in cursor.execute(sql):
                print(r)

    # oracle_client = OracleClient(
    #     host="ebsdb-scan.kinwong.com",
    #     port=1531,
    #     user="hadoop",
    #     password="vSWnGLcdd8ch",
    #     db="prod"
    # )
    #
    # data_list = oracle_client.query("select * from ont.oe_order_lines_all where rownum <= 10")
#     pool = ImpalaClient(
#         host='10.53.0.71',
#         database='impala',
#         user='root',
#         password='',
#         port=21050
#     )

# data_list = pool.query("select * from bi_ods.dw_quality_check_rules ")
#     for data in data_list:
#         print(data)
