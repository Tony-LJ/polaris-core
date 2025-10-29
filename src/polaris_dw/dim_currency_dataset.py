# -*- coding: utf-8 -*-

"""
descr: 生成货币维度表
auther: lj.michale
create_date: 2025/10/28 15:54
file_name: dim_currency_dataset.py
"""

from polaris_common.datetime_utils import get_current_time
import uuid
import pandas as pd

def create_structured_dim_currency():
    """
    生成产品维度表schema
    :return:
    """
    structured_dim_currency = {}
    structured_dim_currency["id"] = uuid.uuid4()

    # etl计算日
    structured_dim_currency["etl_date"] = get_current_time("%Y-%m-%d %H:%M:%S")

    return structured_dim_currency

def generate_dim_currency_dataset():
    """
    生成真实数仓产品维度表
    :return:
    """
    datas = []

    for data in datas:
        datas.append(create_structured_dim_currency(data))

    return pd.DataFrame(datas)


if __name__ == '__main__':
    print(generate_dim_currency_dataset().to_string())

