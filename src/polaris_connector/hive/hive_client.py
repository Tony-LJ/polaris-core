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



if __name__ == '__main__':
    print(" >>>>>>>>>>>>>>>> ")






