# -*- coding: utf-8 -*-

"""
descr: 通用函数
auther: lj.michale
create_date: 2025/9/27 15:54
file_name: general_function.py
"""

def swap_values(x, y):
    """
    交换两个值并返回交换后的结果
    :param x:
    :param y:
    :return: 交换后的两个值组成的元组
    """
    return y, x

def is_leap_year(year):
    """
    判断一个年份是否为闰年
    闰年规则：
    1. 能被4整除但不能被100整除的年份是闰年
    2. 能被400整除的年份是闰年
    3. 其他情况为平年
    参数:
        year (int): 需要判断的年份（正整数）
    返回:
        bool: 是闰年返回True，否则返回False
    异常:
        ValueError: 当输入不是正整数时抛出
    """
    # 验证输入合法性
    if not isinstance(year, int) or year <= 0:
        raise ValueError("年份必须是正整数")
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)


def get_even_numbers(start=1, end=100):
    """
    获取指定范围内（[start, end]）的所有偶数，默认范围为1-100
    参数:
        start (int): 范围起始值（默认1，需为正整数，且小于end）
        end (int): 范围结束值（默认100，需为正整数，且大于start）
    返回:
        list[int]: 范围内所有偶数组成的列表，若参数不合法则返回空列表
    异常提示:
        若start/end非正整数、或start >= end，会打印错误提示
    """
    # 1. 验证输入参数合法性
    # 检查是否为整数
    if not (isinstance(start, int) and isinstance(end, int)):
        print(f"❌ 错误：起始值{start}和结束值{end}必须是整数！")
        return []
    # 检查是否为正整数
    if start <= 0 or end <= 0:
        print(f"❌ 错误：起始值{start}和结束值{end}必须是正整数！")
        return []
    # 检查起始值是否小于结束值
    if start >= end:
        print(f"❌ 错误：起始值{start}必须小于结束值{end}！")
        return []

    even_list = []
    for num in range(start, end + 1):  # range是左闭右开，需+1才能包含end
        if num % 2 == 0:
            even_list.append(num)

    return even_list

