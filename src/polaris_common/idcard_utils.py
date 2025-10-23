# -*- coding: utf-8 -*-

"""
descr: 身份证工具类
auther: lj.michale
create_date: 2025/9/27 15:54
file_name: idcard_utils.py
"""

import re
from datetime import datetime


class IdCardUtils:
    """
    Id Card信息处理类
    """
    def validate_id_card(id_card):
        """
        验证身份证号码的有效性
        :param id_card: 身份证号码字符串
        :return: 如果合法，返回True；否则返回False
        """
        # 验证长度和数字格式
        if not re.match(r"^\d{17}[\dX]$", id_card):
            return False

        # 提取出生日期
        birth_date = id_card[6:14]

        # 验证出生日期的合法性
        try:
            datetime.strptime(birth_date, "%Y%m%d")
        except ValueError:
            return False

        # 计算校验位
        weight_factors = [2**i % 11 for i in range(17)]
        sum_result = sum(int(id_card[i]) * weight_factors[i] for i in range(17))
        check_digit = "10X98765432"[sum_result % 11]

        return id_card[-1] == check_digit

    def parse_id_card_info(id_card):
        """
        从身份证号码中解析出生日期和性别信息
        :param id_card: 身份证号码字符串
        :return: 出生日期和性别的元组
        """
        if not IdCardUtils.validate_id_card(id_card):
            raise ValueError("身份证号码无效")

        # 提取出生日期
        birth_date = id_card[6:14]
        # 提取性别
        gender_code = int(id_card[-2])  # 倒数第二位
        gender = "男" if gender_code % 2 == 1 else "女"

        return birth_date, gender

