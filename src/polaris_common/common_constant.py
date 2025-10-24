# -*- coding: utf-8 -*-

"""
descr: 通用常量
auther: lj.michale
create_date: 2025/9/27 15:54
file_name: common_constant.py
"""

USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36'

# ################################# 时间日期
# 中文月份名称
month_name_cn = ["一月","二月","三月","四月","五月","六月","七月","八月","九月","十月","十一月","十二月"]
# 中文周名称
week_name_cn = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
# 24节气名称
solar_terms_cn = [
    "小寒", "大寒", "立春", "雨水", "惊蛰", "春分", "清明", "谷雨", "立夏", "小满", "芒种", "夏至",
    "小暑", "大暑", "立秋", "处暑", "白露", "秋分", "寒露", "霜降", "立冬", "小雪", "大雪", "冬至"
]
# 12生效
chinese_zodiacs =  ["鼠","牛","虎","兔","龙","蛇","马","羊","猴","鸡","狗","猪"]

# ############################## 正则表达式
# 匹配邮箱：包含大小写字母，下划线，阿拉伯数字，点号，中划线
email_pattern = '[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(?:\.[a-zA-Z0-9_-]+)'
# 匹配身份证：地区： [1-9]\d{5} 年的前两位： (18|19|([23]\d)) 1800-2399 年的后两位： \d{2} 月份： ((0[1-9])|(10|11|12)) 天数： (([0-2][1-9])|10|20|30|31) 闰年不能禁止29+ 三位顺序码： \d{3} 两位顺序码： \d{2} 校验码： [0-9Xx]
id_card_pattern = '[1-9]\d{5}(?:18|19|(?:[23]\d))\d{2}(?:(?:0[1-9])|(?:10|11|12))(?:(?:[0-2][1-9])|10|20|30|31)\d{3}[0-9Xx]'
# 国内手机号码：手机号都为11位，且以1开头，第二位一般为3、5、6、7、8、9 ，剩下八位任意数字
phone_number_cn_pattern = '1(3|4|5|6|7|8|9)\d{9}'
# 国内固定电话：区号3\~4位，号码7\~8位
tel_number_cn_pattern = '\d{3}-\d{8}|\d{4}-\d{7}'
# 域名：包含http:\\或https:\\
domain_pattern = '(?:(?:http:\/\/)|(?:https:\/\/))?(?:[\w](?:[\w\-]{0,61}[\w])?\.)+[a-zA-Z]{2,6}(?:\/)'
# IP地址：IP地址的长度为32位(共有2^32个IP地址)，分为4段，每段8位，用十进制数字表示,每段数字范围为0～255，段与段之间用句点隔开　
ip_pattern = '((?:(?:25[0-5]|2[0-4]\d|[01]?\d?\d)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d?\d))'
# 日期：常见日期格式：yyyyMMdd、yyyy-MM-dd、yyyy/MM/dd、yyyy.MM.dd
datetime_pattern = '\d{4}(?:-|\/|.)\d{1,2}(?:-|\/|.)\d{1,2}'
# 国内邮政编码：我国的邮政编码采用四级六位数编码结构:前两位数字表示省（直辖市、自治区）,第三位数字表示邮区；第四位数字表示县（市）,最后两位数字表示投递局（所）
postal_code_cn_pattern = '[1-9]\d{5}(?!\d)'
# 中文字符：
character_cn_pattern = '[\u4e00-\u9fa5]'
# 验证数字：
digit_pattern = '^[0-9]*$'



# ############################## 时间日期格式
class DatetimeFormat:
    """
    通用日期格式
    """
    DISPLAY_MONTH = '%Y-%m'
    DISPLAY_DATE = '%Y-%m-%d'
    DISPLAY_DT = '%Y-%m-%d %H:%M:%S'

    SUFFIX_DT = '%Y%m%d%H%M%S'
    SUFFIX_DT_UNDERLINE = '%Y_%m_%d_%H_%M_%S'

    SUFFIX_DATE = '%Y%m%d'
    SUFFIX_DATE_UNDERLINE = '%Y_%m_%d'

    SUFFIX_MONTH = '%Y%m'
    SUFFIX_MONTH_UNDERLINE = '%Y_%m'

    SUFFIX_YEAR = '%Y'
    SUFFIX_YEAR_UNDERLINE = '%Y'





if __name__ == '__main__':
    pattern = re.compile(id_card_pattern)

    strs = '小明的身份证号码是342623198910235163，手机号是13987692110'
    result = pattern.findall(strs)

    print(result)
    ['342623198910235163']




