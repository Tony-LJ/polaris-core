# -*- coding: utf-8 -*-


from faker import Faker
from datetime import date
import pandas as pd
import random


# fake = Faker()   # 初始化Faker实例
fake = Faker("zh_CN")

# 模拟生成一个通讯记录的函数
def create_fake_call_record():
    return {
        'caller': fake.phone_number(),
        'recipient': fake.phone_number(),
        'duration': str(random.randint(1, 3600)),  # 假设通话时间从1秒到1小时
        'time': fake.date_time_between(start_date='-1y', end_date='now').strftime('%Y-%m-%d %H:%M:%S'),  # 过去一年里的某个时间点
        'type': random.choice(['incoming', 'outgoing', 'missed'])  # 来电、去电、未接
    }

# 模拟生成一个学信档案的函数
def create_fake_education_record():
    return {
        'name': fake.name(),
        'birth_date': fake.date_of_birth(tzinfo=None, minimum_age=18, maximum_age=30).strftime('%Y-%m-%d'),
        'nationality': fake.country(),
        'university': fake.company(),  # 由于faker没有提供随机大学名的构造 这里用company代替
        'degree': random.choice(['bachelor', 'master', 'phd']),
        'major': fake.job(),
        'enrollment_date': fake.date_between(start_date='-10y', end_date='-4y').strftime('%Y-%m-%d'),
        'graduation_date': fake.date_between(start_date='-4y', end_date='now').strftime('%Y-%m-%d')
    }

# 模拟生成一个信用卡记录的函数
def create_fake_credit_card_transaction():
    return {
        'credit_card_provider': fake.credit_card_provider(),
        'credit_card_number': fake.credit_card_number(),
        'credit_card_security_code': fake.credit_card_security_code(),
        'transaction_date': fake.date_time_between(start_date='-1y', end_date='now').strftime('%Y-%m-%d %H:%M:%S'),
        'transaction_amount': '{:.2f}'.format(random.uniform(1.0, 10000.0)),  # 交易金额
        'currency': fake.currency_code()
    }


# 定义一个函数来创建一个假的个人资料字典
def create_fake_profile():
    profile = {
        "name": fake.name(),
        "age": fake.random_int(min=18, max=80),
        "address": fake.address(),
        "email": fake.email(),
        "username": fake.user_name(),
    }
    return profile


# 定义一个函数来创建假的职业资料
def create_fake_job_info():
    job_info = {
        "company": fake.company(),
        "job_title": fake.job(),
        "department": fake.word(ext_word_list=["HR", "IT", "Sales", "Marketing", "Administration"]),
        "employment_date": fake.date_between(start_date='-5y', end_date='today').strftime('%Y-%m-%d'),
    }
    return job_info


# 定义一个函数来创建联系信息
def create_fake_contact_info():
    contact_info = {
        "phone_number": fake.phone_number(),
        "email": fake.email(),
    }
    return contact_info

# 创建包含个人资料、职业和联系信息的Python结构
def create_structured_profile():
    structured_profile = {
        "personal": create_fake_profile(),
        "job": create_fake_job_info(),
        "contact": create_fake_contact_info(),
    }
    return structured_profile


if __name__ == '__main__':
    # 使用上述函数生成结构化数据
    structured_data = create_structured_profile()
    print(create_fake_call_record())
    print(create_fake_education_record())
    print(create_fake_credit_card_transaction())
    print(structured_data)