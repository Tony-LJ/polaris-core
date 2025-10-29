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

def get_zodiac_sign(month, day):
    if (month == 1 and day >= 20) or (month == 2 and day <= 18):
        return "水瓶座"
    elif (month == 2 and day >= 19) or (month == 3 and day <= 20):
        return "双鱼座"
    elif (month == 3 and day >= 21) or (month == 4 and day <= 19):
        return "白羊座"
    elif (month == 4 and day >= 20) or (month == 5 and day <= 20):
        return "金牛座"
    elif (month == 5 and day >= 21) or (month == 6 and day <= 21):
        return "双子座"
    elif (month == 6 and day >= 22) or (month == 7 and day <= 22):
        return "巨蟹座"
    elif (month == 7 and day >= 23) or (month == 8 and day <= 22):
        return "狮子座"
    elif (month == 8 and day >= 23) or (month == 9 and day <= 22):
        return "处女座"
    elif (month == 9 and day >= 23) or (month == 10 and day <= 23):
        return "天秤座"
    elif (month == 10 and day >= 24) or (month == 11 and day <= 22):
        return "天蝎座"
    elif (month == 11 and day >= 23) or (month == 12 and day <= 21):
        return "射手座"
    else:
        return "摩羯座"

def get_zodiac_year(year):
    """
    根据年份计算生肖
    :param year:
    :return:
    """
    zodiac_animals = [
        "鼠", "牛", "虎", "兔", "龙", "蛇",
        "马", "羊", "猴", "鸡", "狗", "猪"
    ]
    return zodiac_animals[year % 12]

def english_weekday_to_chinese(weekday_en):
    """
    英文星期转中文星期
    :param weekday_en:
    :return:
    """
    weekdays_en_to_cn = {
        "Monday": "星期一",
        "Tuesday": "星期二",
        "Wednesday": "星期三",
        "Thursday": "星期四",
        "Friday": "星期五",
        "Saturday": "星期六",
        "Sunday": "星期日"
    }
    return weekdays_en_to_cn.get(weekday_en, "未知")


if __name__ == '__main__':
    print(get_current_time("timestamp"))
