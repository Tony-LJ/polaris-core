# -*- coding: utf-8 -*-

"""
descr: 生成产品维度表
auther: lj.michale
create_date: 2025/10/28 15:54
file_name: dim_product_dataset.py
"""

from polaris_common.datetime_utils import get_current_time
import uuid
import pandas as pd

def create_structured_dim_product():
    """
    生成产品维度表schema
    :return:
    """
    structured_dim_product = {}
    structured_dim_product["id"] = uuid.uuid4()

    # etl计算日
    structured_dim_product["etl_date"] = get_current_time("%Y-%m-%d %H:%M:%S")

    return structured_dim_product

def generate_dim_product_dataset():
    """
    生成真实数仓产品维度表
    :return:
    """
    datas = []

    for data in datas:
        datas.append(create_structured_dim_product(data))

    return pd.DataFrame(datas)


if __name__ == '__main__':
    print(generate_dim_product_dataset().to_string())

