# -*- coding: utf-8 -*-

"""
descr: hive客户端
auther: lj.michale
create_date: 2025/9/27 15:54
file_name: hive_client.py
"""
from pyhive import hive
import pandas as pd
from typing import Union, List, Optional


class HiveClient:
    """
    Hive数据库连接管理器
    功能：
    - 建立/关闭连接
    - 执行SQL查询（返回DataFrame或原始结果）
    - 基础CRUD操作
    - 数据库元信息查询
    """
    def __init__(self,
                 host: str,
                 port: int = 10000,
                 username: Optional[str] = None,
                 password: Optional[str] = None,
                 database: str = 'default',
                 auth: str = 'NOSASL'):
        """
        初始化连接参数
        :param host: Hive服务器地址
        :param port: 端口号，默认10000
        :param username: 用户名（可选）
        :param password: 密码（可选）
        :param database: 默认数据库，默认'default'
        :param auth: 认证方式，默认'NOSASL'
        """
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.database = database
        self.auth = auth
        self.connection = None

    def __enter__(self):
        """支持with上下文管理"""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """退出上下文时自动关闭连接"""
        self.close()

    def connect(self):
        """建立Hive连接"""
        self.connection = hive.Connection(
            host=self.host,
            port=self.port,
            username=self.username,
            password=self.password,
            database=self.database,
            auth=self.auth
        )
        return self.connection

    def close(self):
        """关闭连接"""
        if self.connection:
            self.connection.close()
            self.connection = None

    def execute(self,
                sql: str,
                return_df: bool = True) -> Union[pd.DataFrame, List[tuple]]:
        """
        执行SQL查询
        :param sql: 要执行的SQL语句
        :param return_df: 是否返回DataFrame，默认True
        :return: DataFrame或原始结果列表
        """
        if not self.connection:
            self.connect()
        try:
            if return_df:
                return pd.read_sql(sql, self.connection)
            else:
                cursor = self.connection.cursor()
                cursor.execute(sql)
                return cursor.fetchall()
        except Exception as e:
            print(f"执行SQL失败: {e}")
            raise

    def create_table(self,
                     table_name: str,
                     columns: dict,
                     partitioned_by: Optional[dict] = None,
                     file_format: str = 'TEXTFILE'):
        """
        创建Hive表
        :param table_name: 表名
        :param columns: 列定义字典 {列名: 类型}
        :param partitioned_by: 分区列定义 {列名: 类型}
        :param file_format: 文件格式，默认'TEXTFILE'
        """
        cols = ', '.join([f"{k} {v}" for k, v in columns.items()])
        sql = f"CREATE TABLE {table_name} ({cols})"

        if partitioned_by:
            parts = ', '.join([f"{k} {v}" for k, v in partitioned_by.items()])
            sql += f" PARTITIONED BY ({parts})"

        sql += f" STORED AS {file_format}"
        self.execute(sql, return_df=False)
        print(f"表 {table_name} 创建成功")


if __name__ == '__main__':
    # 连接配置
    config = {
        'host': '10.53.0.71',
        'port': 10000,
        'username': 'root',
        'password': '',
        'database': 'bi_ads'
    }

    # 执行查询
    with HiveClient(config) as connector:
        # 返回DataFrame
        df = connector.execute("SELECT * FROM bi_ads.ads_ves_archive_report_bi_ds LIMIT 10")
        print(df.head())

        # 返回原始结果
        results = connector.execute("SHOW DATABASES", return_df=False)
        print("数据库列表:", results)


    # with HiveClient(**config) as connector:
    #     # 创建分区表
    #     connector.create_table(
    #         table_name="test_table",
    #         columns={
    #             "id": "INT",
    #             "name": "STRING",
    #             "value": "DOUBLE"
    #         },
    #         partitioned_by={"dt": "STRING"}
    #     )
    #
    #     # 插入数据
    #     test_data = [
    #         {"id": 1, "name": "Alice", "value": 10.5, "dt": "20231025"},
    #         {"id": 2, "name": "Bob", "value": 20.3, "dt": "20231025"}
    #     ]
    #     connector.insert_data("test_table", test_data)



