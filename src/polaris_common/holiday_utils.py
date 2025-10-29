# -*- coding: utf-8 -*-
"""
descr: 接节假日工具类
auther: lj.michale
create_date: 2025/9/19 17:11
file_name: holiday_utils.py
"""
import holidays

class CustomChinaHolidays(holidays.China):
    """
    自定义节假日
    """
    def _populate(self, year):
        super()._populate(year)
        # 添加自定义节日
        self.append({"2024-07-01": "公司成立纪念日"})


if __name__ == '__main__':
    # 创建自定义的中国节假日对象
    custom_cn_holidays = CustomChinaHolidays(years=2024)