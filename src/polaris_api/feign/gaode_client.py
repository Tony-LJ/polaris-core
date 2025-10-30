# -*- coding: utf-8 -*-

"""
descr: 高德客户端
auther: lj.michale
create_date: 2025/9/27 15:54
file_name: gaode_client.py
"""
import requests
from polaris_common.common_constant import public_api_autonavi_key


class GaodeClient:
    def __init__(self):
        self.key = public_api_autonavi_key

    def request_api(self, url):
        re = requests.get(url).json()
        return re

    def get_geocode(self, address):
        """
        地理编码
        :param address:
        :return:
        """
        url = f'https://restapi.amap.com/v3/geocode/geo?parameters&key={self.key}&address={address}'
        json_data = self.request_api(url)
        if json_data['status'] == '1':
            location = json_data['geocodes'][0]['location']
            return location
        else:
            return '获取失败'

    def get_inverse_geocode(self, location):
        """
        根据经纬坐标获取地址等信息
        :param location:
        :return:
        """
        url = f'https://restapi.amap.com/v3/geocode/regeo?parameters&key={self.key}&location={location}'
        json_data = self.request_api(url)
        if json_data['status'] == '1':
            # 获取格式化的详细地址
            formatted_address = json_data['regeocode']['formatted_address']
            return formatted_address
        else:
            return '获取失败'


# if __name__ == '__main__':
#     gd = GaodeClient()
#
#     # 通过坐标获取所在区县
#     area = gd.get_inverse_geocode('113.277732,22.989125')   # 示例经纬度
#     print('area:',area)