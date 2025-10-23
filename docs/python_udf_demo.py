# # -*- coding: utf-8 -*-
#
# """
# descr: Python UDF函数样例
# auther: lj.michale
# create_date: 2025/9/27 15:54
# file_name: python_udf_demo.py
# """
# from odps.udf import annotate
#
# @annotate("string,bigint->string")
# class GetUrlChar(object):
#
#     def evaluate(self, url, n):
#         if n == 0:
#             return ""
#         try:
#             index = url.find(".htm")
#             if index < 0:
#                 return ""
#             a = url[:index]
#             index = a.rfind("/")
#             b = a[index + 1:]
#             c = b.split("-")
#             if len(c) < n:
#                 return ""
#             return c[-n]
#         except Exception:
#             return "Internal error"