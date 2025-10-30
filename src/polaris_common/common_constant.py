# -*- coding: utf-8 -*-

"""
descr: 通用常量
auther: lj.michale
create_date: 2025/9/27 15:54
file_name: common_constant.py
"""
# ################################# 公共API
# 探数
public_api_tanshu = "https://api.tanshuapi.com/api/exchange/v1/index2"
public_api_tanshu_key = "089ec3eb015de8e2fa0a23bb2233cdd8"
# 高德地图
public_api_autonavi_key = "7c3f7032f24c147fa7fce649cc01b374"

# ################################# 数字相关
capital_1to10= ["一","二","三","四","五","六","七","八","九","十"]
traditional_1to10 = ["壹","贰","叁","肆","伍","陆","柒","捌","玖","拾"]

# ################################# 中国文化相关
surname = ["赵","钱","孙","李","周","吴","郑","王","冯","陈","褚","卫","蒋","沈","韩","杨","朱","秦","尤","许"]

# ################################# 网络信息
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36'

# ################################# 地理信息
# 中国省份
province_cn = [
    "北京市", "天津市", "河北省", "山西省", "内蒙古自治区",
    "辽宁省", "吉林省", "黑龙江省", "上海市", "江苏省",
    "浙江省", "安徽省", "福建省", "江西省", "山东省",
    "河南省", "湖北省", "湖南省", "广东省", "广西壮族自治区",
    "海南省", "重庆市", "四川省", "贵州省", "云南省",
    "西藏自治区", "陕西省", "甘肃省", "青海省", "宁夏回族自治区",
    "新疆维吾尔自治区", "香港特别行政区", "澳门特别行政区", "台湾省"
]
# 世界各国中英文名称映射字典
country = {
    'Singapore Rep.':'新加坡',
    'Dominican Rep.':'多米尼加',
    'Palestine':'巴勒斯坦',
    'Bahamas':'巴哈马',
    'Timor-Leste':'东帝汶',
    'Afghanistan':'阿富汗',
    'Guinea-Bissau':'几内亚比绍',
    "Côte d'Ivoire":'科特迪瓦',
    "Br. Indian Ocean Ter.":'英属印度洋领土',
    'Angola':'安哥拉',
    'Albania':'阿尔巴尼亚',
    'United Arab Emirates':'阿联酋',
    'Argentina':'阿根廷',
    'Armenia':'亚美尼亚',
    'French Southern and Antarctic Lands':'法属南半球和南极领地',
    'Australia':'澳大利亚',
    'Austria':'奥地利',
    'Azerbaijan':'阿塞拜疆',
    'Burundi':'布隆迪',
    'Belgium':'比利时',
    'Benin':'贝宁',
    'Burkina Faso':'布基纳法索',
    'Bangladesh':'孟加拉国',
    'Bulgaria':'保加利亚',
    'The Bahamas':'巴哈马',
    'Bosnia and Herz.':'波斯尼亚和黑塞哥维那',
    'Belarus':'白俄罗斯',
    'Belize':'伯利兹',
    'Bermuda':'百慕大',
    'Bolivia':'玻利维亚',
    'Brazil':'巴西',
    'Brunei':'文莱',
    'Bhutan':'不丹',
    'Botswana':'博茨瓦纳',
    'Central African Rep.':'中非',
    'Canada':'加拿大',
    'Switzerland':'瑞士',
    'Chile':'智利',
    'China':'中国',
    'Ivory Coast':'象牙海岸',
    'Cameroon':'喀麦隆',
    'Dem. Rep. Congo':'刚果民主共和国',
    'Congo':'刚果',
    'Colombia':'哥伦比亚',
    'Costa Rica':'哥斯达黎加',
    'Cuba':'古巴',
    'N. Cyprus':'北塞浦路斯',
    'Cyprus':'塞浦路斯',
    'Czech Rep.':'捷克',
    'Germany':'德国',
    'Djibouti':'吉布提',
    'Denmark':'丹麦',
    'Algeria':'阿尔及利亚',
    'Ecuador':'厄瓜多尔',
    'Egypt':'埃及',
    'Eritrea':'厄立特里亚',
    'Spain':'西班牙',
    'Estonia':'爱沙尼亚',
    'Ethiopia':'埃塞俄比亚',
    'Finland':'芬兰',
    'Fiji':'斐',
    'Falkland Islands':'福克兰群岛',
    'France':'法国',
    'Gabon':'加蓬',
    'United Kingdom':'英国',
    'Georgia':'格鲁吉亚',
    'Ghana':'加纳',
    'Guinea':'几内亚',
    'Gambia':'冈比亚',
    'Guinea Bissau':'几内亚比绍',
    'Eq. Guinea':'赤道几内亚',
    'Greece':'希腊',
    'Greenland':'格陵兰',
    'Guatemala':'危地马拉',
    'French Guiana':'法属圭亚那',
    'Guyana':'圭亚那',
    'Honduras':'洪都拉斯',
    'Croatia':'克罗地亚',
    'Haiti':'海地',
    'Hungary':'匈牙利',
    'Indonesia':'印度尼西亚',
    'India':'印度',
    'Ireland':'爱尔兰',
    'Iran':'伊朗',
    'Iraq':'伊拉克',
    'Iceland':'冰岛',
    'Israel':'以色列',
    'Italy':'意大利',
    'Jamaica':'牙买加',
    'Jordan':'约旦',
    'Japan':'日本',
    'Kazakhstan':'哈萨克斯坦',
    'Kenya':'肯尼亚',
    'Kyrgyzstan':'吉尔吉斯斯坦',
    'Cambodia':'柬埔寨',
    'Korea':'韩国',
    'Kosovo':'科索沃',
    'Kuwait':'科威特',
    'Lao PDR':'老挝',
    'Lebanon':'黎巴嫩',
    'Liberia':'利比里亚',
    'Libya':'利比亚',
    'Sri Lanka':'斯里兰卡',
    'Lesotho':'莱索托',
    'Lithuania':'立陶宛',
    'Luxembourg':'卢森堡',
    'Latvia':'拉脱维亚',
    'Morocco':'摩洛哥',
    'Moldova':'摩尔多瓦',
    'Madagascar':'马达加斯加',
    'Mexico':'墨西哥',
    'Macedonia':'马其顿',
    'Mali':'马里',
    'Myanmar':'缅甸',
    'Montenegro':'黑山',
    'Mongolia':'蒙古',
    'Mozambique':'莫桑比克',
    'Mauritania':'毛里塔尼亚',
    'Malawi':'马拉维',
    'Malaysia':'马来西亚',
    'Namibia':'纳米比亚',
    'New Caledonia':'新喀里多尼亚',
    'Niger':'尼日尔',
    'Nigeria':'尼日利亚',
    'Nicaragua':'尼加拉瓜',
    'Netherlands':'荷兰',
    'Norway':'挪威',
    'Nepal':'尼泊尔',
    'New Zealand':'新西兰',
    'Oman':'阿曼',
    'Pakistan':'巴基斯坦',
    'Panama':'巴拿马',
    'Peru':'秘鲁',
    'Philippines':'菲律宾',
    'Papua New Guinea':'巴布亚新几内亚',
    'Poland':'波兰',
    'Puerto Rico':'波多黎各',
    'Dem. Rep. Korea':'朝鲜',
    'Portugal':'葡萄牙',
    'Paraguay':'巴拉圭',
    'Qatar':'卡塔尔',
    'Romania':'罗马尼亚',
    'Russia':'俄罗斯',
    'Rwanda':'卢旺达',
    'W. Sahara':'西撒哈拉',
    'Saudi Arabia':'沙特阿拉伯',
    'Sudan':'苏丹',
    'S. Sudan':'南苏丹',
    'Senegal':'塞内加尔',
    'Solomon Is.':'所罗门群岛',
    'Sierra Leone':'塞拉利昂',
    'El Salvador':'萨尔瓦多',
    'Somaliland':'索马里兰',
    'Somalia':'索马里',
    'Serbia':'塞尔维亚',
    'Suriname':'苏里南',
    'Slovakia':'斯洛伐克',
    'Slovenia':'斯洛文尼亚',
    'Sweden':'瑞典',
    'Swaziland':'斯威士兰',
    'Syria':'叙利亚',
    'Chad':'乍得',
    'Togo':'多哥',
    'Thailand':'泰国',
    'Tajikistan':'塔吉克斯坦',
    'Turkmenistan':'土库曼斯坦',
    'East Timor':'东帝汶',
    'Trinidad and Tobago':'特里尼达和多巴哥',
    'Tunisia':'突尼斯',
    'Turkey':'土耳其',
    'Tanzania':'坦桑尼亚',
    'Uganda':'乌干达',
    'Ukraine':'乌克兰',
    'Uruguay':'乌拉圭',
    'United States':'美国',
    'Uzbekistan':'乌兹别克斯坦',
    'Venezuela':'委内瑞拉',
    'Vietnam':'越南',
    'Vanuatu':'瓦努阿图',
    'West Bank':'西岸',
    'Yemen':'也门',
    'South Africa':'南非',
    'Zambia':'赞比亚',
    'Zimbabwe':'津巴布韦'
}

# ################################# 时间日期
# 中文月份名称
month_name_cn = ["一月","二月","三月","四月","五月","六月","七月","八月","九月","十月","十一月","十二月"]
# 中文周名称
week_name_cn = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
# 24节气名称
solar_terms_cn = ["小寒", "大寒", "立春", "雨水", "惊蛰", "春分", "清明", "谷雨", "立夏", "小满", "芒种", "夏至","小暑", "大暑", "立秋", "处暑", "白露", "秋分", "寒露", "霜降", "立冬", "小雪", "大雪", "冬至"]
solar_terms = {
    "立春": (2, 4),
    "雨水": (2, 19),
    "惊蛰": (3, 5),
    "春分": (3, 20),
    "清明": (4, 4),
    "谷雨": (4, 20),
    "立夏": (5, 5),
    "小满": (5, 21),
    "夏至": (6, 21),
    "小暑": (7, 7),
    "大暑": (7, 22),
    "立秋": (8, 7),
    "处暑": (8, 23),
    "白露": (9, 7),
    "秋分": (9, 23),
    "寒露": (10, 8),
    "霜降": (10, 23),
    "立冬": (11, 7),
    "小雪": (11, 22),
    "大雪": (12, 7),
    "冬至": (12, 21),
    "小寒": (1, 5),
    "大寒": (1, 20)
}
# 12生效
chinese_zodiacs =  ["鼠","牛","虎","兔","龙","蛇","马","羊","猴","鸡","狗","猪"]

# ############################## 正则表达式
# 匹配邮箱：包含大小写字母，下划线，阿拉伯数字，点号，中划线
email_pattern = r'[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(?:\.[a-zA-Z0-9_-]+)'
# 匹配身份证：地区： [1-9]\d{5} 年的前两位： (18|19|([23]\d)) 1800-2399 年的后两位： \d{2} 月份： ((0[1-9])|(10|11|12)) 天数： (([0-2][1-9])|10|20|30|31) 闰年不能禁止29+ 三位顺序码： \d{3} 两位顺序码： \d{2} 校验码： [0-9Xx]
id_card_pattern = r'[1-9]\d{5}(?:18|19|(?:[23]\d))\d{2}(?:(?:0[1-9])|(?:10|11|12))(?:(?:[0-2][1-9])|10|20|30|31)\d{3}[0-9Xx]'
# 国内手机号码：手机号都为11位，且以1开头，第二位一般为3、5、6、7、8、9 ，剩下八位任意数字
phone_number_cn_pattern = r'1(3|4|5|6|7|8|9)\d{9}'
# 国内固定电话：区号3\~4位，号码7\~8位
tel_number_cn_pattern = r'\d{3}-\d{8}|\d{4}-\d{7}'
# 域名：包含http:\\或https:\\
domain_pattern = r'(?:(?:http:\/\/)|(?:https:\/\/))?(?:[\w](?:[\w\-]{0,61}[\w])?\.)+[a-zA-Z]{2,6}(?:\/)'
# IP地址：IP地址的长度为32位(共有2^32个IP地址)，分为4段，每段8位，用十进制数字表示,每段数字范围为0～255，段与段之间用句点隔开　
ip_pattern = r'((?:(?:25[0-5]|2[0-4]\d|[01]?\d?\d)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d?\d))'
# 日期：常见日期格式：yyyyMMdd、yyyy-MM-dd、yyyy/MM/dd、yyyy.MM.dd
datetime_pattern = r'\d{4}(?:-|\/|.)\d{1,2}(?:-|\/|.)\d{1,2}'
# 国内邮政编码：我国的邮政编码采用四级六位数编码结构:前两位数字表示省（直辖市、自治区）,第三位数字表示邮区；第四位数字表示县（市）,最后两位数字表示投递局（所）
postal_code_cn_pattern = r'[1-9]\d{5}(?!\d)'
# 中文字符：
character_cn_pattern = r'[\u4e00-\u9fa5]'
# 验证数字：
digit_pattern = r'^[0-9]*$'

# ############################## DataOps相关配置
gitlab_url = "https://git.example.com"
gitlab_private_token = "xxxxxxxxxxxxxxxxxx"



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









