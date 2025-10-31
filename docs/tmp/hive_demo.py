# -*- coding: utf-8 -*-

from pyhive import hive

# 读取数据
def test_connection(sql):
    # 创建hive连接
    conn = hive.Connection(host='10.53.0.71', # HiveServer2主机的IP地址
                           port=10000, # HiveServer2服务端口号
                           username='root', # 连接hive数据库的用户名
                           database='bi_ads', # 具体数据库名
                           auth='NOSASL' # 客户端的认证模式
                           )
    cur = conn.cursor()
    # 执行查询
    cur.execute(sql)
    # 获取查询结果
    results = cur.fetchall()
    return results

sql = "show tables"
res = test_connection(sql)
print(res)