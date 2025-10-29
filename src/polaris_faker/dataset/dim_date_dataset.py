# -*- coding: utf-8 -*-

"""
descr: 生成日期维度表
auther: lj.michale
create_date: 2025/10/28 15:54
file_name: dim_date_dataset.py
"""
import uuid
import pandas as pd
from polaris_common.datetime_utils import get_zodiac_year, get_zodiac_sign


def get_day_record(day):

    return day

def create_structured_dim_date(date):
    """
    生成日期维度表schema
    :param id:
    :param date:
    :return:
    """
    structured_dim_date = {}
    structured_dim_date["id"] = uuid.uuid4()
    # 日期-年月日(yyyy-MM-dd)
    structured_dim_date["day"] = date
    # 年月(yyyy-MM)
    structured_dim_date["year_month"] = date.strftime("%Y-%m")
    # 月(MM)
    structured_dim_date["month"] = date.strftime("%m")
    # 年(yyyy)
    structured_dim_date["year"] = date.strftime("%Y")
    # 年生肖
    structured_dim_date["zodiac"] = get_zodiac_year(date.year)
    # 星座
    structured_dim_date["aries"] = get_zodiac_sign(date.month,date.day)
    # 当年年初(yyyy-MM-dd HH:mm:ss)
    structured_dim_date["year_first_day"] = ""
    # 当年年末(yyyy-MM-dd HH:mm:ss)
    structured_dim_date["year_last_day"] = ""
    # 当月月初(yyyy-MM-dd HH:mm:ss)
    structured_dim_date["month_first_day"] = ""
    # 当月月末(yyyy-MM-dd HH:mm:ss)
    structured_dim_date["month_last_day"] = ""
    # 当日日初(yyyy-MM-dd HH:mm:ss)
    structured_dim_date["day_first_day"] = ""
    # 当日日末(yyyy-MM-dd HH:mm:ss)
    structured_dim_date["day_last_day"] = ""
    # 本月第几天
    structured_dim_date["day_n_month"] = ""
    # 星期(数字)
    structured_dim_date["week_day"] = ""
    # 当年第几周
    structured_dim_date["week_n_year"] = ""
    # 年周
    structured_dim_date["year_week"] = ""
    # 季度
    structured_dim_date["season"] = ""
    # 是否工作日
    structured_dim_date["is_work_day"] = ""
    # 是否节假日
    structured_dim_date["is_holiday"] = ""
    # etl计算日
    structured_dim_date["etl_date"] = ""

    return structured_dim_date

def generate_dim_date_dataset(start_date='2000-01-01', end_date='2025-12-31'):
    """
    生成真实数仓日期维度表
    :param start_date: 开始日期
    :param end_date: 结束日期
    :return:
    """
    datas = []
    for date in pd.date_range(start=start_date,end=end_date):
        datas.append(create_structured_dim_date(date))

    return pd.DataFrame(datas)


if __name__ == '__main__':
    print(generate_dim_date_dataset("2025-01-01", "2025-12-31").to_string())