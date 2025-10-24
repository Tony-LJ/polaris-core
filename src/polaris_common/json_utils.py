# -*- coding: utf-8 -*-

"""
descr: JSON操作工具类
auther: lj.michale
create_date: 2025/9/27 15:54
file_name: json_utils.py
"""
import pandas as pd


class JsonUtils:

    @staticmethod
    def json_to_df(json_data):
        """
         將JSON深度嵌套的结构展平为二维表格
        :param self:
        :param json_data:
        :param sep:
        :return:
        """
        df = pd.json_normalize(json_data, sep="_")

        return df






# if __name__ == '__main__':
#     data = [
#         {"id": 1, "info": {"name": "Alice", "age": 30}, "hobbies": ["reading", "cycling"]},
#         {"id": 2, "info": {"name": "Bob", "age": 25}, "hobbies": ["gaming"]}
#     ]
#     data2 = {
#         "name": "Alice",
#         "age": 30,
#         "is_student": False,
#         "courses": ["Math", "Physics"],
#         "address": None
#     }
#
#     df = JsonUtils.json_to_df(data2)
#     print(df)