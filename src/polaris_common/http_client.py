# -*- coding: utf-8 -*-

"""
descr : http请求模块封装
auther : lj.michale
create_date : 2025/9/27 15:54
file_name : http_client.py
"""
import json
import logging
import requests


class HttpClient:
    def __init__(self):
        # 设置日志记录器
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)


    def request(self, method, url, headers=None, params=None, data=None):
        response = requests.request(method, url, headers=headers, params=params, data=data)
        return response.status_code, response.text

    def get(self, url, headers=None, params=None):
        return self.request('GET', url, headers=headers, params=params)

    def post(self, url, headers=None, data=None):
        if headers is None:
            headers = {}
        if data is not None and 'Content-Type' not in headers:
            headers['Content-Type'] = 'application/json'
            data = json.dumps(data)
        return self.request('POST', url, headers=headers, data=data)