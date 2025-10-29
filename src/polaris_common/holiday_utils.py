# -*- coding: utf-8 -*-
"""
descr: 接节假日工具类
auther: lj.michale
create_date: 2025/9/19 17:11
file_name: holiday_utils.py
"""
import holidays
# from common_constant import solar_terms
from datetime import datetime
from chinese_calendar import is_workday

def is_workdays(date):
    """
    # 判断是否是法定节假日
    """
    if is_workday(date):
        return "工作日"
    else:
        return "休息日"


# def get_solar_term(date):
#     for term, (month, day) in solar_terms.items():
#         if (date.month == month and date.day >= day) or (date.month == (month % 12 + 1) and date.day < solar_terms[term][1]):
#             return term
#     return "未找到节气"


# class CustomChinaHolidays(holidays.China):
#     """
#     自定义节假日
#     """
#     def _populate(self, year):
#         super()._populate(year)
#         # 添加自定义节日
#         self.append({"2024-07-01": "公司成立纪念日"})

if __name__ == '__main__':
    date_1 = datetime.now().date()
    print("date_1: {}, type: {}".format(date_1, type(date_1)))
    print(is_workdays(date_1))

# if __name__ == '__main__':
#     # 创建自定义的中国节假日对象
#     # custom_cn_holidays = CustomChinaHolidays(years=2024)
#     date = datetime(2023, 3, 10)
    # print(get_solar_term(date))
    # print(get_solar_term("2024-07-01"))