# -*- coding: utf-8 -*-

"""
descr: 人的信息数据集
auther: lj.michale
create_date: 2025/10/30 15:54
file_name: person_dataset.py
"""
from faker import Faker
from datetime import date
import pandas as pd
import random

from polaris_common.common_constant import province_cn
from polaris_common.common_constant import country as world_country
from polaris_common.common_utils import CommonUtils

# fake = Faker()   # 初始化Faker实例
fake = Faker("zh_CN")


def create_fake_country_record(country='中国'):
    """
    生成国家记录
    :param country:
    :return:
    """
    country = fake.country()
    country_code = fake.country_code()
    return country, country_code



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

    return structured_person

def get_gis_dataset(data_size, ration):
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
    gis_dataset = get_gis_dataset(100,0)
    print(gis_dataset.to_string())



