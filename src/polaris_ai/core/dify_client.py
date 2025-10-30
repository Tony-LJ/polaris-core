# -*- coding: utf-8 -*-

"""
descr: Dify client客户端
auther: lj.michale
create_date: 2025/10/18 09:54
file_name: dify_client.py
"""
import requests
import os
import mimetypes
import json
from typing import Optional
import argparse


class DifyClient:

    def __init__(self,
                 api_key: str,
                 base_url: str,
                 user_id: str):
        """
        初始化
        :param api_key:
        :param base_url:
        :param user_id:
        """
        self.api_key = api_key
        self.base_url = base_url
        self.user_id = user_id

