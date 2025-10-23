# -*- coding: utf-8 -*-

"""
descr: influxdb时序数据客户端封装
auther: lj.michale
create_date: 2025/9/27 15:54
file_name: influxdb_client.py
"""
import logging
from influxdb import InfluxDBClient
from polaris_common import CommonUtils

class InfluxdbClient:
    """
    influxdb工具类
    conf_influx = {
       'host': '110.110.110.110',
       'port': 8086,
       'username': 'admin',
       'password': '123456',
       'database': 'db_test',
    }
   """
    TZ = "tz('Asia/Shanghai')"
    CONN = None
    CFID = None

    @classmethod
    def _init(cls, conf: dict):
        if cls.CONN is None:
            cls.connect(conf)
        elif cls.CFID != CommonUtils.get_uuid(conf):
            cls.connect(conf)

    @classmethod
    def connect(cls, conf: dict):
        try:
            cls.CONN = InfluxDBClient(**conf)
            cls.CFID = CommonUtils.get_uuid(conf)
        except Exception as e:
            logging.error("influxdb init failed, please check the config", e)

    @classmethod
    def exec_sql(cls, conf: dict, sql: str):
        """
        执行influxdb查询sql
        :param conf:
        :param sql:
        :return:
        """
        cls._init(conf)
        return list(cls.CONN.query(sql).get_points())

    @classmethod
    def write_data(cls, conf: dict, tbl: str, data_list: list):
        """
        向influxdb写入数据
        :data_list 格式：[(time, tid, v1, v2, ...), ...]
        """
        cls._init(conf)
        json_data_list = []
        for data in data_list:
            fields = {}
            for i, v in enumerate(data[2:], 1):
                fields[f'v{i}'] = round(v, 3)
            json_data = {
                'measurement': tbl,
                'time': str(data[0]).replace(' ', 'T') + '+08:00',
                'tags': {
                    'tid': str(data[1])
                },
                'fields': fields,
            }
            json_data_list.append(json_data)
        cls.CONN.write_points(json_data_list)

    @classmethod
    def write_points(cls, conf: dict, json_data_list: list):
        """向influxdb写入数据
        :json_data_list 格式：[{
            'measurement': 'tbl',
            'time': time.replace(' ', 'T') + '+08:00',
            'tags': {
                'k': 'v'
            },
            'fields': {'k': 'v'},
        }, ...]
        """
        cls._init(conf)
        cls.CONN.write_points(json_data_list)

    @classmethod
    def create_db(cls, conf: dict, db_name: str):
        """
        关闭数据库
        :param conf:
        :param db_name:
        :return:
        """
        cls._init(conf)
        cls.CONN.create_database(db_name)
