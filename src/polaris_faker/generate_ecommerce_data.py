# -*- coding: utf-8 -*-

"""
descr: 生成电商数据
auther: lj.michale
create_date: 2025/9/27 15:54
file_name: generate_ecommerce_data.py
"""
from faker import Faker
from datetime import date
import pandas as pd
import random

# fake = Faker()   # 初始化Faker实例
fake = Faker("zh_CN")


def _generate_ids(data_sizes, ration):
    """
    定义生成可重复ID的函数，其中参数ration为重复的ID占比，比如0.3
    :param data_sizes:
    :param ration:
    :return:
    """
    # 计算重复的id数
    num_dupl = int(data_sizes*ration)
    # 先生成一部分不重复的id
    ids = [str(fake.uuid4()) for _ in range(data_sizes - num_dupl)]
    # 随机抽取一部分id来重复
    ids.extend(random.sample(ids, num_dupl))
    # 打乱顺序
    random.shuffle(ids)

    return ids


def generate_order_dataset_func(data_sizes, ration):
    """
    模拟生成电商行业销售数据
    :param data_sizes:
    :param ration:
    :return:
    """
    datas = []
    ids = _generate_ids(data_sizes, ration)

    for id in ids:
        # 生成用户名字
        name = fake.name()
        # 生成用户邮箱
        email = fake.email()
        # 生成商品名称
        product_name = fake.word()
        producct_categories = ['A', 'B', 'C', 'D', 'E']   # 方法一：手动定义
        category = random.choice(producct_categories)
        # 生成购买数量
        quantity = random.randint(1,10)
        # 生成单价。使用uniform生成50~200之间的随机浮动数，并使用round保留两位小数
        unit_price = round(random.uniform(50,200), 2)
        # 生成同消费金额
        total_price = round(quantity*unit_price, 2)
        # 随机生成2024上半年这个时间段的购买日期
        sale_date = fake.date_between(start_date=date(2024,1,1), end_date=date(2024,6,30))

        datas.append({
            'id': id,
            'name': name,
            'email': email,
            'product_name': product_name,
            'category': category,
            'quantity': quantity,
            'unit_price': unit_price,
            'total_price': total_price,
            'sale_date': sale_date
        })

    return pd.DataFrame(datas)  # 将数据转化为DataFrame形式，作为返回值

# if __name__ == '__main__':
    data_size = 1000   # 确定要造的数据数量
    ration = 0.3   # 确定重复比例
    df = generate_order_dataset_func(data_size, ration)
    print(df)
    # 查找 'id' 列中重复的行
    print(df[df.duplicated(subset='id')])