# -*- coding: utf-8 -*-
"""
descr: 正则表达式工具类
auther: lj.michale
create_date: 2025/9/19 17:11
file_name: regex_utils.py
"""

import re

class RegexUtils:

    @staticmethod
    def match_pattern(pattern, string):
        """
        正则匹配
        :param pattern:
        :param string:
        :return:
        """
        return re.match(pattern, string)

    @staticmethod
    def search_pattern(pattern, string):
        """
        从字符串中提取符合模式的部分
        :param pattern:
        :param string:
        :return:
        """
        return re.search(pattern, string)

    @staticmethod
    def find_all(pattern, string):
        """
        正则查找所有
        :param pattern:
        :param string:
        :return:
        """
        return re.findall(pattern, string)

    @staticmethod
    def replace_pattern(pattern, repl, string):
        """
        正则替换
        :param pattern:
        :param repl:
        :param string:
        :return:
        """
        return re.sub(pattern, repl, string)






