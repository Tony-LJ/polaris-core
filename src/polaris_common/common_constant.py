# -*- coding: utf-8 -*-

"""
descr: 通用常量
auther: lj.michale
create_date: 2025/9/27 15:54
file_name: common_constant.py
"""

USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36'

# 中文月份名称
ch_month_name = [
    "一月",
    "二月",
    "三月",
    "四月",
    "五月",
    "六月",
    "七月",
    "八月",
    "九月",
    "十月",
    "十一月",
    "十二月",
]

# 中文周名称
ch_week_name = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]

class DatetimeFormat:
    """
    通用日期格式
    """
    DISPLAY_MONTH = '%Y-%m'
    DISPLAY_DATE = '%Y-%m-%d'
    DISPLAY_DT = '%Y-%m-%d %H:%M:%S'

    SUFFIX_DT = '%Y%m%d%H%M%S'
    SUFFIX_DT_UNDERLINE = '%Y_%m_%d_%H_%M_%S'

    SUFFIX_DATE = '%Y%m%d'
    SUFFIX_DATE_UNDERLINE = '%Y_%m_%d'

    SUFFIX_MONTH = '%Y%m'
    SUFFIX_MONTH_UNDERLINE = '%Y_%m'

    SUFFIX_YEAR = '%Y'
    SUFFIX_YEAR_UNDERLINE = '%Y'










