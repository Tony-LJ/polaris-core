# -*- coding: utf-8 -*-

"""
descr: 通用常量
auther: lj.michale
create_date: 2025/9/27 15:54
file_name: common_constant.py
"""
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36'
# 中文月份名称
month_name_cn = ["一月","二月","三月","四月","五月","六月","七月","八月","九月","十月","十一月","十二月"]
# 中文周名称
week_name_cn = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
# 24节气名称
solar_terms_cn = [
    "小寒", "大寒", "立春", "雨水", "惊蛰", "春分", "清明", "谷雨", "立夏", "小满", "芒种", "夏至",
    "小暑", "大暑", "立秋", "处暑", "白露", "秋分", "寒露", "霜降", "立冬", "小雪", "大雪", "冬至"
]
# 12生效
chinese_zodiacs =  ["鼠","牛","虎","兔","龙","蛇","马","羊","猴","鸡","狗","猪"]


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










