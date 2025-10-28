# -*- coding: utf-8 -*-
"""
descr: 日期处理工具类
auther: lj.michale
create_date: 2025/9/19 17:11
file_name: datetime_utils.py
"""
from datetime import datetime
import pytz


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

def get_datetime_timezone(iso_str, time_zone, format):
    """
     时区转换计算
    :param iso_str:
    :param time_zone: Asia/Shanghai
    :param format: %Y-%m-%d, %H:%M:%S %Z
    :return:
    """
    # 解析ISO 8601字符串并设置为UTC时区
    utc_dt = ''
    if iso_str is None:
        utc_dt = datetime.fromisoformat(str("2099-10-05T14:30:00")).replace(tzinfo=pytz.utc)
    else:
        utc_dt = datetime.fromisoformat(str(iso_str)).replace(tzinfo=pytz.utc)
    # 定义目标时区（例如CST，即中国标准时间）
    cst_tz = pytz.timezone(time_zone)
    # 将UTC时间转换为CST时间
    cst_dt = utc_dt.astimezone(cst_tz)
    formatted_datetime_str = cst_dt.strftime(format)

    return formatted_datetime_str


if __name__ == '__main__':
    print(get_current_time("timestamp"))
