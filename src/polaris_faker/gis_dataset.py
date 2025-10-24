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

def get_gis_dataset(data_size, ration):
    datas = []
    ids = generate_ids(data_size, ration)

    for id in ids:
        country = '中国'
        country_code = fake.country_code()
        province = fake.random_element(elements=province_cn)
        address = fake.address()
        datas.append({
            'id': id,
            'country': country,
            'province': province,
            'country_code': country_code,
            'address': address,
        })

    return pd.DataFrame(datas)


if __name__ == '__main__':
    data_size = 100   # 确定要造的数据数量
    ration = 0   # 确定重复比例
    df = get_gis_dataset(data_size, ration)
    print(df.to_string())




