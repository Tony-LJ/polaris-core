# -*- coding: utf-8 -*-
"""
descr: 日期处理工具类
auther: lj.michale
create_date: 2025/9/19 17:11
file_name: datetime_utils.py
"""
from datetime import datetime


def get_current_time(format):
    """
    获取当前日期或者时间戳
    :param format: "%Y-%m-%d %H:%M:%S"
    :return:
    """
    current_time = datetime.now()
    formatted_time = None
    if format != "timestamp":
        formatted_time = current_time.strftime(format)
    elif format == "timestamp":
        formatted_time = current_time.timestamp()

    return formatted_time



if __name__ == '__main__':
    print(get_current_time("timestamp"))
