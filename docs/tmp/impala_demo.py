# -*- coding: utf-8 -*-

from impala.dbapi import connect

# 建立与 Impala 的连接
conn = connect(host='10.53.0.71', port=21050,user='root',password='',database='impala')
cursor = conn.cursor()

# 创建表（如必要）
cursor.execute("CREATE TABLE IF NOT EXISTS bi_tmp.test_table (id INT, name STRING)")

# 准备要插入的数据
data_to_insert = [(1, 'Alice'), (2, 'Bob'), (3, 'Cathy')]

# 插入数据
for record in data_to_insert:
    cursor.execute("INSERT INTO bi_tmp.test_table (id, name) VALUES (%s, %s)", record)

# 提交更改
conn.commit()

# 查询以验证数据是否插入
cursor.execute("SELECT * FROM bi_tmp.test_table")
rows = cursor.fetchall()
for row in rows:
    print(row)

# 关闭连接
cursor.close()
conn.close()
# -*- coding: utf-8 -*-