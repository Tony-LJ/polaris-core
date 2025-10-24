# -*- coding: utf-8 -*-

"""
descr: 模拟生成人的信息数据集
auther: lj.michale
create_date: 2025/10/30 15:54
file_name: person_dataset.py
"""
from faker import Faker
from datetime import date
import pandas as pd
import random

from polaris_common.common_utils import CommonUtils

# fake = Faker()   # 初始化Faker实例
fake = Faker("zh_CN")

def generate_name_record(name='中国'):
    """
    生成姓名记录
    :param name:
    :return:
    """
    name = "张珊"
    return name

def generate_age_record(age=18):
    """
    生成年龄记录
    :param age:
    :return:
    """
    age = 18
    return age

def generate_sex_record(sex='男'):
    """
    生成性别记录
    :param sex:
    :return:
    """
    sex = 18
    return sex

def create_structured_person(id):
    """
     创建人信息结构类型
     type=1 => 国家、省、市、县、镇、街道，详细地址信息,etc
    :param country:
    :param province:
    :param city:
    :param county:
    :param type:
    :return:
    """
    structured_person = {}
    structured_person["id"] = id
    structured_person["name"] = generate_name_record()
    structured_person["age"] = generate_age_record()
    structured_person["sex"] = generate_sex_record()

    return structured_person

def generate_person_dataset(data_size, ration):
    """
    模拟生成person dataset
    :param data_size:
    :param ration:
    :return:
    """
    datas = []
    ids  =CommonUtils.generate_ids(15,100,0)

    for id in ids:
        datas.append(create_structured_person(id))

    return pd.DataFrame(datas)


if __name__ == '__main__':
    data_size = 100   # 确定要造的数据数量
    ration = 0   # 确定重复比例
    # structured_gis = create_structured_gis()
    # print(structured_gis)
    gis_dataset = generate_person_dataset(100,0)
    print(gis_dataset.to_string())



