# -*- coding: utf-8 -*-
"""
descr : 时间通用工具模块
auther : zengsg
create_date : 2025/10/10 15:20
file_name : string_convert.py
desc: 字符串转和 datetime对象 互相转换
"""


import time
from datetime import datetime, timedelta, timezone
from typing import Optional, Union
import logging

class TimeHandler :
    def __init__(self):
        # 设置日志记录器
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    @staticmethod
    def str_to_datetime(
            time_str: str,
            time_format: str = "%Y-%m-%d %H:%M:%S",
            time_zone: Optional[Union[str, int]] = None,
    ) -> Optional[datetime]:
        """
        字符串转datetime对象
        :param time_str: 时间字符串（如"2023-10-01 12:00:00"）
        :param time_format: 时间格式（默认"%Y-%m-%d %H:%M:%S"）
        :return: datetime对象，转换失败返回None
        """
        try:
            return datetime.strptime(time_str, time_format)
        except (ValueError,TypeError):
             logging.error(f"时间字符串转换失败：{time_str}")
             return None

    @staticmethod
    def datetime_to_str(
            dt: datetime,
            fmt: str = "%Y-%m-%d %H:%M:%S"
    ) -> Optional[str]:
        """
        datetime对象转字符串
        :param dt: datetime对象
        :param fmt: 目标格式（默认"%Y-%m-%d %H:%M:%S"）
        :return: 格式化字符串，输入无效返回None
        """
        if not isinstance(dt, datetime):
            return None
        try:
            return dt.strftime(fmt)
        except ValueError:
            logging.error(f"时间字符串转换失败：{dt}")
            return None

    @staticmethod
    def timestamp_to_datetime(
            timestamp: Union[int, float],
            is_millisecond: bool = False
    ) -> Optional[datetime]:
        """
        时间戳转datetime对象
        :param timestamp: 时间戳（10位秒级/13位毫秒级）
        :param is_millisecond: 是否为毫秒级（13位），默认False（秒级）
        :return: datetime对象，输入无效返回None
        """
        try:
            # 毫秒级时间戳需转为秒级（除以1000）
            if is_millisecond:
                timestamp = timestamp / 1000
            return datetime.fromtimestamp(timestamp)
        except (TypeError, ValueError):
            logging.error(f"时间戳转换失败：{timestamp}")
            return None

    @staticmethod
    def datetime_to_timestamp(
            dt: datetime,
            is_millisecond: bool = False
    ) -> Optional[Union[int, float]]:
        """
        datetime对象转时间戳
        :param dt: datetime对象
        :param is_millisecond: 是否返回毫秒级（13位），默认False（10位秒级）
        :return: 时间戳，输入无效返回None
        """
        if not isinstance(dt, datetime):
            return None
        try:
            timestamp = dt.timestamp()
            return int(timestamp * 1000) if is_millisecond else int(timestamp)
        except OSError:
            logging.error(f"时间戳转换失败：{dt}")
            return None

    @staticmethod
    def str_to_timestamp(
            time_str: str,
            fmt: str = "%Y-%m-%d %H:%M:%S",
            is_millisecond: bool = False
    ) -> Optional[Union[int, float]]:
        """
        字符串转时间戳（组合str_to_datetime和datetime_to_timestamp）
        :param time_str: 时间字符串
        :param fmt: 时间格式
        :param is_millisecond: 是否返回毫秒级
        :return: 时间戳，转换失败返回None
        """
        dt = TimeHandler.str_to_datetime(time_str, fmt)
        return TimeHandler.datetime_to_timestamp(dt, is_millisecond) if dt else None

    # ------------------------------
    # 2. 时间计算：加减、差值
    # ------------------------------
    @staticmethod
    def add_time(
            dt: datetime,
            days: int = 0,
            hours: int = 0,
            minutes: int = 0,
            seconds: int = 0,
    ) -> datetime:
        """
        对datetime对象加减时间
        :param dt: 原始datetime对象
        :param days: 加减的天数（可为负数）
        :param hours: 加减的小时数
        :param minutes: 加减的分钟数
        :param seconds: 加减的秒数
        :return: 计算后的datetime对象，输入无效返回None
        """

        if not isinstance(dt, datetime):
            logging.error(f"add_time：输入无效的datetime对象：{dt}")
            return None
        try:
            return dt + timedelta(
                days=days, hours=hours, minutes=minutes, seconds=seconds
            )
        except OverflowError:
            logging.error(f"add_time：时间超出范围：{dt}")
            return None

    @staticmethod
    def time_diff(
            dt1: datetime,
            dt2: datetime,
            unit: str = "seconds"
    ) -> Optional[Union[int, float]]:
        """
        计算两个时间的差值
        :param dt1: 时间1（被减数）
        :param dt2: 时间2（减数）
        :param unit: 结果单位：seconds（秒）、minutes（分）、hours（时）、days（天）
        :return: 差值（dt1 - dt2），输入无效返回None
        """
        if not (isinstance(dt1, datetime) and isinstance(dt2, datetime)):
            logging.error(f"time_diff：输入无效的datetime对象：{dt1}、{dt2}")
            return None
        # 计算两个时间点的差值，返回一个 timedelta 对象
        diff = dt1 - dt2
        # units 字典定义了不同时间单位的转换
        units = {
            "seconds": diff.total_seconds(),
            "minutes": diff.total_seconds() / 60,
            "hours": diff.total_seconds() / 3600,
            "days": diff.days + diff.seconds / 86400
        }
        return units.get(unit, None)
