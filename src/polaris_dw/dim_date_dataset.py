# -*- coding: utf-8 -*-

"""
descr: 生成日期维度表
auther: lj.michale
create_date: 2025/10/28 15:54
file_name: dim_date_dataset.py
"""

import calendar
import uuid
import pandas as pd
from polaris_common.datetime_utils import get_zodiac_year, get_zodiac_sign, english_weekday_to_chinese, \
    get_current_time, is_valid_date, get_lunar_dt
from datetime import timedelta
import holidays
from datetime import datetime
from dateutil.rrule import rrule, DAILY
from polaris_common.holiday_utils import is_workdays
from polaris_connector.impala.impala_client import ImpalaClient

cn_holidays = holidays.China()

def create_structured_dim_date(date):
    """
    生成日期维度表schema
    :param date:
    :return:
    """
    structured_dim_date = {}
    structured_dim_date["id"] = str(uuid.uuid4()).replace('-', '')
    # 公历日期-年月日(yyyy-MM-dd)
    structured_dim_date["day"] = date
    # 公历日期-年月日(yyyyMMdd)
    structured_dim_date["day2"] = date.strftime("%Y%m%d")
    # 24节气
    # structured_dim_date["solar_term"] = get_solar_term(date)
    # 农历日期-年月日(yyyy-MM-dd)
    structured_dim_date["lunar_date"] = get_lunar_dt(date.strftime('%Y-%m-%d'))
    # 年月(yyyy-MM)
    structured_dim_date["year_month"] = date.strftime("%Y-%m")
    # 月(MM)
    structured_dim_date["month"] = date.strftime("%m")
    # 年(yyyy)
    structured_dim_date["year"] = date.strftime("%Y")
    # 年所属生肖
    structured_dim_date["zodiac"] = get_zodiac_year(date.year)
    # 星座
    structured_dim_date["aries"] = get_zodiac_sign(date.month,date.day)
    # 当年年初(yyyy-MM-dd HH:mm:ss)
    structured_dim_date["year_first_day"] = datetime(date.year, 1, 1).strftime("%Y-%m-%d %H:%M:%S")
    # 当年年末(yyyy-MM-dd HH:mm:ss)
    structured_dim_date["year_last_day"] = (datetime(date.year, 12, 31) + timedelta(days=1) - timedelta(seconds=1)).strftime("%Y-%m-%d %H:%M:%S")
    # 当月月初(yyyy-MM-dd HH:mm:ss)
    structured_dim_date["month_first_day"] = date.replace(day=1).strftime("%Y-%m-%d %H:%M:%S")
    # 当月月末(yyyy-MM-dd HH:mm:ss)
    structured_dim_date["month_last_day"] = (date.replace(day=calendar.monthrange(date.year, date.month)[1]) + timedelta(days=1) - timedelta(seconds=1)).strftime("%Y-%m-%d %H:%M:%S")
    # 当日日初(yyyy-MM-dd HH:mm:ss)
    structured_dim_date["day_first_day"] = date.replace(hour=0, minute=0, second=0, microsecond=0).strftime("%Y-%m-%d %H:%M:%S")
    # 当日日末(yyyy-MM-dd HH:mm:ss)
    structured_dim_date["day_last_day"] = (date.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1) - timedelta(seconds=1)).strftime("%Y-%m-%d %H:%M:%S")
    # 当年第几天
    structured_dim_date["day_n_year"] = str(date.timetuple().tm_yday)
    # 当月第几天
    structured_dim_date["day_n_month"] = str((date - date.replace(day=1)).days + 1)
    # 星期
    structured_dim_date["week_day"] = english_weekday_to_chinese(date.strftime("%A"))
    # 当年第几周
    structured_dim_date["week_n_year"] = str(date.isocalendar().week)
    # 季度
    structured_dim_date["quarter"] = str((date.month - 1) // 3 + 1)
    # 是否工作日
    structured_dim_date["is_work_day"] = is_workdays(date)
    # 是否节假日
    structured_dim_date["is_holiday"] = cn_holidays.get(pd.Timestamp(date))
    # etl计算日
    structured_dim_date["etl_date"] = get_current_time("%Y-%m-%d %H:%M:%S")

    return structured_dim_date

def generate_dim_date_dataset(start_datetime, end_datetime):
    """
    生成真实数仓日期维度表
    :param start_date: 开始日期
    :param end_date: 结束日期
    :return:
    """
    date_list = list(rrule(DAILY, dtstart=start_datetime, until=end_datetime))
    valid_date_tmp_array = []
    for date in date_list:
        valid_date_tmp_array.append(date.strftime('%Y-%m-%d'))

    datas = []
    valid_date_array = [date for date in valid_date_tmp_array if is_valid_date(date)]
    for date_str in valid_date_array:
        datas.append(create_structured_dim_date(datetime.strptime(date_str, "%Y-%m-%d")))

    return pd.DataFrame(datas)


if __name__ == '__main__':
    current_year = datetime.strptime(get_current_time("%Y-%m-%d"), "%Y-%m-%d").year
    current_month =  datetime.strptime(get_current_time("%Y-%m-%d"), "%Y-%m-%d").month
    current_day =  datetime.strptime(get_current_time("%Y-%m-%d"), "%Y-%m-%d").day

    # print(generate_dim_date_dataset(datetime(2015, 1, 1), datetime(2025, 12, 31)).to_string())
    df = generate_dim_date_dataset(datetime(2015, 1, 1), datetime(current_year, current_month, current_day))
    pool = ImpalaClient(
        host='10.53.0.71',
        database='impala',
        user='root',
        password='',
        port=21050
    )
    insert_sql = f''' INSERT INTO bi_data.dim_date_ds (
                 id
                ,day
                ,day2
                ,lunar_date
                ,year_month
                ,month
                ,year
                ,zodiac
                ,aries
                ,year_first_day
                ,year_last_day
                ,month_first_day
                ,month_last_day
                ,day_first_day
                ,day_last_day
                ,day_n_year
                ,day_n_month
                ,week_day
                ,week_n_year
                ,quarter
                ,is_work_day
                ,is_holiday
                ,etl_date
                ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                '''
    conn = pool._get_conn()
    cursor = conn.cursor()
    cursor.execute("TRUNCATE TABLE bi_data.dim_date_ds")
    print(df.apply(tuple, axis=1).tolist())

    for record in df.apply(tuple, axis=1).tolist():
        cursor.execute(insert_sql, record)


