# -*- coding: utf-8 -*-
"""
descr : HTTP客户端调用方法枚举
auther : lj.michale
create_date : 2025/10/27 15:54
file_name : http_method_enums.py
"""

from enum import Enum

class HttpMethodEnums(Enum):
    GET = "GET"
    POST = "POST"
    PATCH = "PATCH"
    PUT = "PUT"
    DELETE = "DELETE"
    HEAD = "HEAD"
    OPTIONS = "OPTIONS"