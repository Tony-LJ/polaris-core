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
        return datetime.now()

    @staticmethod
    def format_datetime(dt, format_string):
        return dt.strftime(format_string)


    @staticmethod
    def add_days(dt, days):
        return dt + timedelta(days=days)

    @staticmethod
    def days_between(date1, date2):
        delta = date2 - date1
        return delta.days