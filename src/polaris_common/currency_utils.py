# -*- coding: utf-8 -*-

"""
descr: 货币工具类
auther: lj.michale
create_date: 2025/10/23 15:54
file_name: currency_utils.py
"""
from http_client import HttpClient
from polaris_common.common_constant import public_api_tanshu, public_api_tanshu_key

def get_exchange_rate(dict):
    data = http_client.get(url=public_api_tanshu,params=dict).json
    return data['data']["money"]

def convert_currency(amount, currency='CNY'):
    """
    计算货币汇率
    :param amount:
    :param currency:
    :return:
    """
    if currency == 'CNY':
        target_currency = 'USD'
        exchange_rate = get_exchange_rate(target_currency)
        converted_amount = amount / exchange_rate
    else:
        target_currency = 'CNY'
        exchange_rate = get_exchange_rate(target_currency)
        converted_amount = amount * exchange_rate
    return converted_amount


if __name__ == '__main__':
    http_client = HttpClient()
    dict = {'key': public_api_tanshu_key,'from': 'CNY', 'to': 'USD', 'money': 1}
    print(http_client.get(url=public_api_tanshu,params=dict).text)