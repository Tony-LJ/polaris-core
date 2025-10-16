# -*- coding: utf-8 -*-
"""
descr: 文本处理工具类
auther: lj.michale
create_date: 2025/9/19 17:11
file_name: polaris_string_utils.py
"""

class PolarisStringUtils:

    @staticmethod
    def to_uppercase(s):
        """
        静态方法,可以直接通过类名调用，而不需要实例化类
        转大写字母
        :param s:
        :return:
        """
        return s.upper()

    @staticmethod
    def to_lowercase(s):
        """
        转小写字母
        :param s:
        :return:
        """
        return s.lower()

    @staticmethod
    def reverse_string(s):
        """
        颠倒字符串顺序
        :param s:
        :return:
        """
        return s[::-1]