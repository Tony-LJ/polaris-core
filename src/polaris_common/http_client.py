# -*- coding: utf-8 -*-

"""
descr : http请求模块封装
auther : lj.michale
create_date : 2025/9/27 15:54
file_name : http_client.py
"""

from  polaris_logger import logger
import requests
from requests.exceptions import RequestException, HTTPError


class HttpClient:
    def __init__(self, base_url):
        self.base_url = base_url
        # 设置日志记录器
        self.logger = logger.getLogger(__name__)
        self.logger.setLevel(logger.DEBUG)
        handler = logger.StreamHandler()
        formatter = logger.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def _request(self, method, path, **kwargs):
        url = self.base_url + path
        try:
            response = requests.request(method, url, **kwargs)
            response.raise_for_status()  # 检查HTTP错误
            return response.json()  # 假设返回的是JSON数据
        except HTTPError as http_err:
            self.logger.error(f"HTTP error occurred: {http_err}")
        except RequestException as err:
            self.logger.error(f"Request failed: {err}")
        except Exception as e:
            self.logger.error(f"An error occurred: {e}")
        return None

    def get(self, path, params=None):
        return self._request('GET', path, params=params)

    def post(self, path, json=None, data=None):
        return self._request('POST', path, json=json, data=data)
