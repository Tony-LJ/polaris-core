# -*- coding: utf-8 -*-

"""
descr : 字符串处理通用模块
auther : zengsg
create_date : 2025/10/10 15:20
file_name : string_convert.py
desc: 空值判断（StringUtils.isEmpty()）、脱敏（手机号 / 身份证隐藏）、格式转换等

"""

import json
import logging

class StringConvert:

    def __init__(self):
        # 设置日志记录器
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    @staticmethod
    def is_empty(self, value):
        """
        判断字符串是否为空（None或空字符串）
        :param value: 待判断的字符串
        :return: 如果字符串为空则返回True，否则返回False
        """
        return value is None or value.strip() == ""

    @staticmethod
    def mask_phone(self, phone):
        """
        手机号隐藏
        :param phone: 手机号
        :return: 隐藏后的手机号
        """
        if self.is_empty(phone):
            return phone
        return phone[:3] + "****" + phone[-4:]

    @staticmethod
    def mask_id_card(self, id_card):
        """
        身份证隐藏
        :param id_card: 身份证号码
        :return: 隐藏后的身份证号码
        """
        if self.is_empty(id_card):
            return id_card
        return id_card[:2] + "**********" + id_card[-2:]

    @staticmethod
    def json_to_dict(self, json_str):
        """
        将JSON字符串转换为字典
        :param json_str: JSON字符串
        :return: 字典
        """
        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            self.logger.error(f"JSON字符串转换失败：{e}")
            return {}

    @staticmethod
    def dict_to_json(self, dic):
        """
        将字典转换为JSON字符串
        :param dic: 字典
        :return: JSON字符串
        """
        try:
            return json.dumps(dic, ensure_ascii=False)
        except Exception as e:
            self.logger.error(f"字典转换JSON字符串失败：{e}")
            return "{}"