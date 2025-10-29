# -*- coding: utf-8 -*-

"""
descr: 生成日期维度表
auther: lj.michale
create_date: 2025/10/28 15:54
file_name: dim_date_dataset.py
"""
import pandas as pd

def create_structured_dim_date(id):
    """
    生成日期维度表schema
    :return:
    """
    structured_dim_date = {}
    structured_dim_date["id"] = id
    # 日期-年月日(yyyy-MM-dd)
    structured_dim_date["day"] = ""
    # 年月(yyyy-MM)
    structured_dim_date["year_month"] = ""
    # 月(MM)
    structured_dim_date["month"] = ""
    # 年(yyyy)
    structured_dim_date["year"] = ""
    # 当月月初
    structured_dim_date["month_first_day"] = ""
    # 当月月末
    structured_dim_date["month_last_day"] = ""
    # 当日日初
    structured_dim_date["day_first_day"] = ""
    # 当日日末
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

def generate_dim_date_dataset(data_size=100, ration=0):
    """
    模拟生成产品库存的信息数据集
    :param data_size:
    :param ration:
    :return:
    """
    datas = []
    ids = ""

    for id in ids:
        datas.append(create_structured_dim_date(id))

    return pd.DataFrame(datas)
