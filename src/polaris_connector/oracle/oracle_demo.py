# -*- coding: utf-8 -*-

import oracledb

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
    for result in cursor.execute("select t.ORG_ID,t.LINE_ID,TO_CHAR(t.REQUEST_DATE, 'YYYY-MM-DD HH24:MI:SS') from ont.oe_order_lines_all t where ROWNUM <= 10"):
        print(result)

# 释放连接池
pool.release(oapool)

# 关闭连接池
pool.close()

