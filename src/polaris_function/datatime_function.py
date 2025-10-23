# -*- coding: utf-8 -*-

"""
descr: 时间日期通用函数
auther: lj.michale
create_date: 2025/9/27 15:54
file_name: datatime_function.py
"""
from datetime import datetime, timedelta
from polaris_common import DatetimeFormat
from datetime import datetime, date, timedelta
import numpy as np
import pandas as pd

# 基本时间差
delta = timedelta(
    days=1,
    hours=24,
    minutes=30,
    seconds=60
)

def is_leap_year(year):
    """
    判断一个年份是否为闰年
    闰年规则：
    1. 能被4整除但不能被100整除的年份是闰年
    2. 能被400整除的年份是闰年
    3. 其他情况为平年
    参数:
        year (int): 需要判断的年份（正整数）
    返回:
        bool: 是闰年返回True，否则返回False
    异常:
        ValueError: 当输入不是正整数时抛出
    """
    # 验证输入合法性
    if not isinstance(year, int) or year <= 0:
        raise ValueError("年份必须是正整数")
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)


