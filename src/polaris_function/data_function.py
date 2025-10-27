# -*- coding: utf-8 -*-

"""
descr: 数字操作通用函数
auther: lj.michale
create_date: 2025/9/27 15:54
file_name: data_function.py
"""
import math
import random
import numpy as np


class DatatimeFunction:

    def sample_weighted(ll, weights, k):
        """
        带权重、非重复取样
        :param ll:
        :param weights:
        :param k:
        :return:
        """
        ll_len = len(ll)
        if ll_len < k:
            raise ValueError(f"len(ll)={ll_len}<{k}")
        elif ll_len == k:
            return random.sample(ll, k)
        else:
            new_ll = list(range(len(ll)))
            new_ll_set = set(new_ll)
            new_weights = np.array(weights)
            new_k = k
            result_tot = []
            while True:
                result = random.choices(new_ll, weights=new_weights[new_ll], k=new_k)
                result_set = set(result)
                result_tot.extend(result_set)
                new_ll_set -= result_set
                new_k = k - len(result_tot)
                new_ll = list(new_ll_set)
                if new_k == 0:
                    break

            result_tot.sort()
            if isinstance(ll, np.ndarray):
                ret = ll[result_tot]
            else:
                ret = [ll[_] for _ in result_tot]

            return ret

    @staticmethod
    def range_partition(max, partitions=10, min=0):
        """根据数据范围划分区间
        :param min 最小值，默认值0
        :param max 最大值
        :param partitions 划分的区间数
        :return 返回划分后的区间集合 ['区间1', '区间2', '区间3', ...]
        """
        res = []
        interval = max / partitions

        while len(res) < partitions:
            start, end = min, min + interval
            res.append(f'{start:.1f} ~ {end:.1f}') if end < max else res.append(f'>= {min:.1f}')
            min += interval

        return res

# @staticmethod
# def date_partition(freq, start_time, end_time):
#     """根据数据频率划分时间区间
#     :param freq 数据频率
#     :return 返回划分后的时间区间集合 {}
#     """
#     res = {}
#     begin = DtUtil.day_start_of_date_str(start_time)
#     end = DtUtil.day_end_of_date_str(end_time)
#     while begin < end:
#         res[begin] = None
#         begin = begin + relativedelta(seconds=freq)
#     return res
#
# @staticmethod
# def day_start_of_date_str(src_dt_str: str, src_df: str = DF_STD_SEC):
#     """获取某一天的起始时间
#     @param src_dt_str:日期字符串
#     @param src_df:源日期字符串格式
#     @return 某一天的起始时间
#     """
#     d1 = DtUtil.convert_str_to_date(src_dt_str, src_df)
#     return DtUtil.convert_str_to_date(DtUtil.convert_date_to_str(d1, DtUtil.DF_STD_DAY), DtUtil.DF_STD_DAY)
#
# @staticmethod
# def day_end_of_date_str(src_dt_str: str, src_df: str = DF_STD_SEC):
#     """获取某一天的结束时间，即第二天的开始时间
#     @param src_dt_str:源日期字符串
#     @param src_df:源日期字符串格式
#     @return 某一天的起始时间
#     """
#     d1 = DtUtil.convert_str_to_date(src_dt_str, src_df) + relativedelta(days=1)
#     return DtUtil.convert_str_to_date(DtUtil.convert_date_to_str(d1, DtUtil.DF_STD_DAY), DtUtil.DF_STD_DAY)
#


