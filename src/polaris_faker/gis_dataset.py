# -*- coding: utf-8 -*-

"""
descr: 地理信息数据集
auther: lj.michale
create_date: 2025/10/30 15:54
file_name: gis_dataset.py
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

def generate_ids(data_size, ration):
    """
    定义生成可重复ID的函数，其中参数ration为重复的ID占比，比如0.3
    :param data_size:
    :param ration:
    :return:
    """
    num_dupl = int(data_size*ration)
    ids = [str(fake.uuid4()) for _ in range(data_size - num_dupl)]
    ids.extend(random.sample(ids, num_dupl))
    random.shuffle(ids)

    return ids

def create_fake_country_record(country='中国'):
    print("生成国家记录")

def create_fake_province_record(province='湖南省'):
    print("生成省份记录")

def create_fake_city_record(city='常德市'):
    print("生成市区记录")

def create_fake_county_record(county='桃源县'):
    print("生成县级记录")

def create_fake_address_record(country='中国', province='湖南省', city='常德市', county='桃源县'):
    print("生成详细地址信息记录")

def create_structured_gis(country, province, city, county):
    """
     创建GIS地理信息结构类型
     type=1 => 国家、省、市、县、镇、街道，详细地址信息,etc
    :param country:
    :param province:
    :param city:
    :param county:
    :param type:
    :return:
    """
    structured_gis = {}
    structured_gis["country"] = create_fake_country_record()
    structured_gis["province"] = create_fake_province_record()
    structured_gis["city"] = create_fake_city_record()
    structured_gis["county"] = create_fake_county_record()
    structured_gis["address"] = create_fake_address_record()


def get_gis_dataset(data_size, ration):
    datas = []
    ids = generate_ids(data_size, ration)

    for id in ids:
        country = '中国'
        country_code = fake.country_code()
        province = fake.random_element(elements=province_cn)
        city = ""
        address = fake.address()
        datas.append({
            'id': id,
            'country': country,
            'province': province,
            'city': city,
            'country_code': country_code,
            'address': address,
        })

    return pd.DataFrame(datas)



if __name__ == '__main__':
    data_size = 100   # 确定要造的数据数量
    ration = 0   # 确定重复比例
    df = get_gis_dataset(data_size, ration)
    print(df.to_string())



