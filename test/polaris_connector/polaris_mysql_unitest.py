# -*- coding: utf-8 -*-

from polaris_connector.mysql import MysqlClient

# 初始化连接池
pool = MysqlClient(
    host='10.53.0.71',
    database='bigdata',
    user='root',
    password='LJkwhadoop2025!',
    port=3306
)


if __name__ == '__main__':
    table_output = f"ODS_CUX_INV_MIC"
    data = pool.query("SELECT * FROM dask_ods_meta")
    print(data)


