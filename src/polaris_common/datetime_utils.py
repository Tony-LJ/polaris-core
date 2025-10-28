# -*- coding: utf-8 -*-
"""
descr: 日期处理工具类
auther: lj.michale
create_date: 2025/9/19 17:11
file_name: datetime_utils.py
"""
from datetime import datetime


class DatetimeUtils:
    """
    日期处理类
    """
    def __init__(self,datetime,format):
        self.datetime = datetime
        self.format = format

    def get_current_time(self,format):
        """
        获取当前日期
        :param format: "%Y-%m-%d %H:%M:%S"
        :return:
        """
        current_time = datetime.now()
        formatted_time = current_time.strftime(format)

        return formatted_time


