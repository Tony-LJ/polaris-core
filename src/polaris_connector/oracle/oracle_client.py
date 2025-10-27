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


oracledb.init_oracle_client(lib_dir=r"D:\software\oracle\instantclient_23_9")  # 针对oracle11.2的老版本需要采用这种厚模式
# 使用连接池的方法,目的是可以提高数据库的性能
# 初始化连接
pool = oracledb.create_pool(user="hadoop",
                            password='vSWnGLcdd8ch',
                            dsn="ebsdb-scan.kinwong.com:1531/prod",
                            min=2,
                            max=5,
                            increment=1)

# Acquire 连接到池
oapool = pool.acquire()
# 使用连接池
with oapool.cursor() as cursor:
    # for result in cursor.execute("select * from ont.oe_order_lines_all t where ROWNUM <= 10"):
    for result in cursor.execute("select t.ORG_ID"
                                 ",t.LINE_ID"
                                 ",TO_CHAR(t.REQUEST_DATE, 'YYYY-MM-DD HH24:MI:SS') as REQUEST_DATE"
                                 ",TO_CHAR(t.PROMISE_DATE, 'YYYY-MM-DD HH24:MI:SS') as PROMISE_DATE"
                                 ",TO_CHAR(t.ACTUAL_FULFILLMENT_DATE, 'YYYY-MM-DD HH24:MI:SS') as ACTUAL_FULFILLMENT_DATE"
                                 " from ont.oe_order_lines_all t where ROWNUM <= 100"):
        column_names = [desc[0] for desc in cursor.description]
        print("Column Names:", column_names)
        print(result)

# 释放连接池
pool.release(oapool)

# 关闭连接池
pool.close()
