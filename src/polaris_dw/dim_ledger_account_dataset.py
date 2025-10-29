# -*- coding: utf-8 -*-

"""
descr: 生成会计科目维度表
auther: lj.michale
create_date: 2025/10/28 15:54
file_name: dim_ledger_account_dataset.py
"""

from polaris_common.datetime_utils import get_current_time
import uuid
import pandas as pd

def create_structured_dim_ledger_account():
    """
    生成会计科目维度表schema
    :return:
    """
    structured_dim_ledger_account = {}
    structured_dim_ledger_account["id"] = uuid.uuid4()

    # etl计算日
    structured_dim_ledger_account["etl_date"] = get_current_time("%Y-%m-%d %H:%M:%S")

    return structured_dim_ledger_account

def generate_dim_ledger_account_dataset():
    """
    生成真实数仓会计科目维度表
    :return:
    """
    datas = []

    for data in datas:
        datas.append(create_structured_dim_ledger_account(data))

    return pd.DataFrame(datas)


if __name__ == '__main__':
    print(generate_dim_ledger_account_dataset().to_string())

