# -*- coding: utf-8 -*-
"""
descr: 日期处理工具类
auther: lj.michale
create_date: 2025/9/19 17:11
file_name: date_time_utils.py
"""
from datetime import datetime, timedelta


class DateTimeUtils:
    @staticmethod
    def current_datetime():
        """
        获取当前日期
        :return:
        """
        return datetime.now()

    @staticmethod
    def format_datetime(dt, format_string):
        """
        日期格式化
        :param dt:
        :param format_string:
        :return:
        """
        return dt.strftime(format_string)

    @staticmethod
    def add_days(dt, days):
        """
        日期加法
        :param dt:
        :param days:
        :return:
        """
        return dt + timedelta(days=days)

    @staticmethod
    def days_between(date1, date2):
        """
        计算日期差
        :param date1:
        :param date2:
        :return:
        """
        delta = date2 - date1
        return delta.days