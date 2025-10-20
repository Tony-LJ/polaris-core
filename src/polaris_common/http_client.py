# -*- coding: utf-8 -*-

"""
descr : 同步HTTP客户端
auther : lj.michale
create_date : 2025/9/27 15:54
file_name : http_client.py
"""

import requests
from datetime import timedelta
from enum import Enum
from polaris_enums import HttpMethodEnums as HttpMethod

class HttpClient:
    """
    descr: 同步HTTP客户端
    通过request封装，实现了常见的HTTP方法,支持设置超时时间、请求参数等，链式调用
    Examples:
        >>> HttpClient().get("http://www.baidu.com").text
        >>> HttpClient().get("http://www.google.com", params={"name": "hui"}).bytes
        >>> HttpClient().post("http://www.google.com", data={"name": "hui"}).json
    Attributes:
        default_timeout: 默认请求超时时间,单位秒
        default_headers: 默认请求头字典
        client: request 客户端
        response: 每次实例请求的响应
    """

    def __init__(self, timeout=timedelta(seconds=10), headers: dict = None):
        """构造异步HTTP客户端"""
        self.default_timeout = timeout
        self.default_headers = headers or {}
        self.client = requests.session()
        self.response: requests.Response = None

    def _request(
            self,
            method: HttpMethod, url: str,
            params: dict = None, data: dict = None,
            timeout: timedelta = None, **kwargs
    ):
        """内部请求实现方法
        创建客户端会话,构造并发送HTTP请求,返回响应对象
        Args:
            method: HttpMethod 请求方法, 'GET', 'POST' 等
            url: 请求URL
            params: 请求查询字符串参数字典
            data: 请求体数据字典
            timeout: 超时时间,单位秒
            kwargs: 其他关键字参数
        Returns:
            httpx.Response: HTTP响应对象
        """
        timeout = timeout or self.default_timeout
        headers = self.default_headers or {}
        self.response = self.client.request(
            method=method.value,
            url=url,
            params=params,
            data=data,
            headers=headers,
            timeout=timeout.total_seconds(),
            **kwargs
        )
        return self.response

    @property
    def json(self):
        return self.response.json()

    @property
    def bytes(self):
        return self.response.content

    @property
    def text(self):
        return self.response.text

    def get(self, url: str, params: dict = None, timeout: timedelta = None, **kwargs):
        """GET请求
        Args:
            url: 请求URL
            params: 请求查询字符串参数字典
            timeout: 请求超时时间,单位秒
        Returns:
            self 自身对象实例
        """

        self._request(HttpMethod.GET, url, params=params, timeout=timeout, **kwargs)
        return self

    def post(self, url: str, data: dict = None, timeout: timedelta = None, **kwargs):
        """POST请求
        Args:
            url: 请求URL
            data: 请求体数据字典
            timeout: 请求超时时间,单位秒
        Returns:
            self 自身对象实例
        """
        self._request(HttpMethod.POST, url, data=data, timeout=timeout, **kwargs)
        return self

    async def put(self, url: str, data: dict = None, timeout: timedelta = None, **kwargs):
        """PUT请求
        Args:
            url: 请求URL
            data: 请求体数据字典
            timeout: 请求超时时间,单位秒
        Returns:
            self 自身对象实例
        """
        self._request(HttpMethod.PUT, url, data=data, timeout=timeout, **kwargs)
        return self

    async def delete(self, url: str, data: dict = None, timeout: timedelta = None, **kwargs):
        """DELETE请求
        Args:
            url: 请求URL
            data: 请求体数据字典
            timeout: 请求超时时间,单位秒
        Returns:
            self 自身对象实例
        """
        self._request(HttpMethod.DELETE, url, data=data, timeout=timeout, **kwargs)
        return self


# if __name__ == '__main__':
#     url = "https://juejin.cn/"
#     http_client = HttpClient()
#     for i in range(2):
#         text_content = http_client.get(url).text
#         print(text_content)
#
#
#     print(http_client.get(url='https://h.moyanjdc.top').text)