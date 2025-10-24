# -*- coding: utf-8 -*-

"""
descr: 模拟生成产品的信息数据集
auther: lj.michale
create_date: 2025/10/30 15:54
file_name: product_dataset.py
"""
from faker import Faker
from datetime import date
import pandas as pd
import random

from polaris_common.common_utils import CommonUtils

# fake = Faker()   # 初始化Faker实例
fake = Faker("zh_CN")

def generate_product_name_record(product_name='水果'):
    """
    生成产品名称记录
    :param name:
    :return:
    """
    product_name = "张珊"
    return product_name

def create_structured_product(id):
    """
    生成产品信息结构
    :return:
    """
    structured_product = {}
    structured_product["id"] = id
    structured_product["product_name"] = generate_product_name_record()

    return structured_product

def generate_product_dataset(data_size=100, ration=0):
    """
    模拟生成person dataset
    :param data_size:
    :param ration:
    :return:
    """
    datas = []
    ids = CommonUtils.generate_ids(15,data_size,ration)

    for id in ids:
        datas.append(create_structured_product(id))

    return pd.DataFrame(datas)


if __name__ == '__main__':
    data_size = 1000   # 确定要造的数据数量
    ration = 0   # 确定重复比例
    gis_dataset = generate_product_dataset(data_size,ration)
    print(gis_dataset.to_string())



