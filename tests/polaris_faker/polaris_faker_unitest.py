# -*- coding: utf-8 -*-


from faker import Faker

from collections import OrderedDict

# fake = Faker(["en_US", "zh_CN", "ja_JP"])

fake = Faker(["zh_CN"])

# print(fake.name())

# print(fake['en-US'].name())

# print(fake.company())


# 1、使用？#自定义规则，随机生成字符串

print(fake.bothify()) # 默认生成字符串格式： 05 RW

print(fake.bothify(text="666????####", letters='我们的家')) # letters的字符串随机给text的？使用，##默认数字代替，格式如： 我我的我4777


# 2、使用^自定义规则，随机生成16进制字符串

print(fake.hexify(text='MAC Address: ^^:^^:^^:^^:^^:^^', upper=True)) # MAC Address: CD:18:FC:9F:B6:49


# 3、随机生成 i18n 语言的代码

print(fake.language_code()) # yo


# 4、使用？自定义规则，随机生成ASCII字符串

print(fake.lexify(text='Random Identifier: ??????????', letters='我ABCDE')) # Random Identifier: CBC我DD我ABE


# 5、随机生成 i18n 区域设置

print(fake.locale()) # zh_CH


# 6、使用#！@%自定义规则，随机生成字符串

print(fake.numerify(text='# @!! @ %')) # 1 98 7 （#=[0,9] %=[1,9] !=随机数字或空字符 @=非0数字或空字符）


# 7、随机选择对象元素，并随机生成列表

print(fake.random_choices(elements=('a', 'b', 'c', 'd'), length=10)) # ['a', 'c', 'c', 'd', 'a', 'd', 'd', 'b', 'b', 'a']

print(fake.random_choices(elements=OrderedDict([("a", 0.45), ("b", 0.35), ("c", 0.15), ("d", 0.05), ]))) # ['b', 'c', 'a', 'a']


# 8、随机生成0-9整数

print(fake.random_digit()) # 0


# 9、随机生成1-9整数

print(fake.random_digit_not_null()) # 1


# 10、随机生成0-9整数或空值

print(fake.random_digit_or_empty()) # ""


# 11、随机选择元素，默认可重复、长度为1

print(fake.random_element(elements=('a', 'b', 'c', 'd'))) # a

print(fake.random_element(elements=OrderedDict([("a", 0.45), ("b", 0.35), ("c", 0.15), ("d", 0.05), ]))) # a


# 12、随机选择元素，默认可重复、长度不定

print(fake.random_elements(elements=('a', 'b', 'c', 'd'), unique=False))

print(fake.random_elements(elements=OrderedDict([("a", 0.45), ("b", 0.35), ("c", 0.15), ("d", 0.05), ]), length=20, unique=False))


# 13、在指定范围内，随机生成整数

print(fake.random_int(min=0, max=15, step=3))


# 14、随机生成ASCII字符串 [a-zA-Z]

print(fake.random_letter()) # 'y'


# 15、随机生成ASCII字符串列表 [a-zA-Z]

print(fake.random_letters(length=10)) # ['R', 'N', 'v', 'n', 'A', 'v', 'O', 'p', 'y', 'E']


# 16、随机生成ASCII小写字符串

print(fake.random_lowercase_letter()) # c


# 17、随机生成整数

'''
如果digits为None(默认值)，则取值范围为1 ~ 9之间的随机整数。
如果fix_len为False(默认值)，则可以生成所有不超过位数的整数。
如果fix_len为True，则只能生成具有精确位数的整数。
'''

print(fake.random_number(fix_len=True)) # 297371

print(fake.random_number(digits=3, fix_len=False)) # 577


# 18、随机生成元素不重复的不超出元素数量的列表

print(fake.random_sample(elements=('a', 'b', 'c', 'd', 'f', 'f'), length=6)) # 元素可相同，但length不能大于6


# 19、生成大写字母的ASCII字符串

print(fake.random_uppercase_letter())


# 20、随机生成接近某个数字的整数

'''
如果le为False(默认值)，则允许生成数量的140%。如果为True，则上限生成为100%。
如果ge为False(默认值)，则允许生成数量减少到60%。如果为True，下限生成上限为100%。
如果提供了最小值的数值，则生成的小于最小值的值将被固定在最小值。
如果为max提供了一个数值，则生成的大于max的值将被固定在max。
如果le和ge都为True，则number的值将自动返回，而不管提供的min和max的值是什么。
'''

print(fake.randomize_nb_elements(number=100)) # 83

print(fake.randomize_nb_elements(number=100, le=True, ge=True, min=80)) # 100


# 21、随机生成地址和邮政编号

print(fake.address())


# 22、随机生成门牌号

print(fake.building_number())


# 23、随机生成城市

print(fake.city())


# 24、随机生成特殊市

print(fake.city_suffix())


# 25、随机生成国家

print(fake.country())


# 26、随机生成国家编号

print(fake.country_code())


# 27、生成当前国家

print(fake.current_country())


# 28、生成当前国家编号

print(fake.current_country_code())


# 29、随机生成邮编

print(fake.postcode())


# 30、随机生成街道地址

print(fake.street_address())


# 31、随机生成街道名称

print(fake.street_name())


# 32、随机生成街道名称后缀

print(fake.street_suffix())


# 33、随机生成汽车供应商牌照

print(fake.license_plate()) # 974-XXRA


# 34、生成ABA的路由传输号

print(fake.aba())


# 35、生成银行提供商的ISO 3166-1 alpha-2国家代码

print(fake.bank_country()) # GB


# 36、生成基本银行帐号(BBAN)

print(fake.bban()) # MAAN00447407504564


# 37、生成国际银行账号(IBAN)

print(fake.iban())


# 38、生成SWIFT代码

print(fake.swift(length=11, primary=True, use_dataset=True)) # SVWBGBNKXXX


# 39、生成11位的SWIFT代码

print(fake.swift11(use_dataset=True)) # SVWBGBNKXXX


# 40、生成8位的SWIFT代码

print(fake.swift8(use_dataset=True))


# 41、生成EAN码

print(fake.ean(prefixes=('45', '49'), length=13)) # 4532804944052


# 42、生成EAN13码

print(fake.ean13(prefixes=('45', '49'))) # 4518561138095


# 43、生成EAN8码

print(fake.ean8(prefixes=('45', '49'))) # 45877841


# 44、生成指定长度的本地化EAN条码

print(fake.localized_ean(length=8))


# 45、生成指定长度的本地化EAN13条码

print(fake.localized_ean13())


# 46、生成指定长度的本地化EAN8条码

print(fake.localized_ean8())


# 47、生成随机颜色值

print(fake.color(hue='red'))

print(fake.color(luminosity='light'))

print(fake.color(hue=(100, 200), color_format='rgb'))

print(fake.color(hue='orange', luminosity='bright'))

print(fake.color(hue=135, luminosity='dark', color_format='hsv'))

print(fake.color(hue=(300, 20), luminosity='random', color_format='hsl'))


# 48、随机生成颜色名称

print(fake.color_name())


# 49、生成一个十六进制三元组格式的颜色

print(fake.hex_color())


# 50、生成一个以逗号分隔的RGB值格式的颜色

print(fake.rgb_color())


# 51、用CSS rgb()函数生成颜色格式

print(fake.rgb_css_color())


# 52、生成一个网络安全的颜色名称

print(fake.safe_color_name())


# 53、生成一个网络安全的颜色格式为十六进制三重

print(fake.safe_hex_color())


# 54、公司相关(技术\思想\名称...)

print(fake.bs()) # leverage plug-and-play networks

print(fake.catch_phrase())

print(fake.company())

print(fake.company_suffix())


# 55、信用卡相关

print(fake.credit_card_expire()) # 09/28

print(fake.credit_card_full()) # 'Discover\nKatherine Fisher\n6587647593824218 05/26\nCVC: 892\n'

print(fake.credit_card_number()) # 6504876475938248

print(fake.credit_card_provider()) # VISA 19 digit

print(fake.credit_card_security_code()) # 604


# 56、货币相关

print(fake.cryptocurrency())

print(fake.cryptocurrency_code())

print(fake.cryptocurrency_name())

print(fake.currency())

print(fake.currency_code())

print(fake.currency_name())

print(fake.currency_symbol())

print(fake.pricetag())


# 57、时间相关

print(fake.am_pm())

print(fake.century())

print(fake.date())

print(fake.date_between())

print(fake.date_between_dates())

print(fake.date_object())

print(fake.date_of_birth())

print(fake.date_this_century())

print(fake.date_this_decade())

print(fake.date_this_month())

print(fake.date_this_year())

print(fake.date_time())

print(fake.date_time_ad())

print(fake.date_time_between())

print(fake.date_time_between_dates())

print(fake.date_time_this_century())

print(fake.date_time_this_decade())

print(fake.date_time_this_month())

print(fake.date_time_this_year())

print(fake.day_of_month())

print(fake.day_of_week())

print(fake.future_date())

print(fake.future_datetime())

print(fake.iso8601())

print(fake.month())

print(fake.month_name())

print(fake.past_date())

print(fake.past_datetime())

print(fake.pytimezone())

print(fake.time())

print(fake.time_delta())

print(fake.time_object())

print(fake.time_series())

print(fake.timezone())

print(fake.unix_time())

print(fake.year())


# 58、文件相关

print(fake.file_extension())

print(fake.file_extension(category='image'))

print(fake.file_name(category='audio'))

print(fake.file_name(extension='abcdef'))

print(fake.file_name(category='audio', extension='abcdef'))

print(fake.file_path(depth=3))

print(fake.file_path(depth=5, category='video'))

print(fake.file_path(depth=5, category='video', extension='abcdef'))

print(fake.mime_type())

print(fake.mime_type(category='application'))

print(fake.unix_device())

print(fake.unix_device(prefix='mmcblk'))

print(fake.unix_partition())

print(fake.unix_partition(prefix='mmcblk'))


# 59、陆地坐标数据

print(fake.coordinate())

print(fake.latitude())

print(fake.latlng())

print(fake.local_latlng())

print(fake.location_on_land())

print(fake.longitude())


# 60、因特网相关

print(fake.ascii_company_email()) # 邮箱

print(fake.ascii_email()) # ascii邮箱

print(fake.ascii_free_email())

print(fake.ascii_safe_email())

print(fake.company_email()) # 公司邮箱

print(fake.dga()) # 网址

print(fake.domain_name()) # 网址

print(fake.domain_word())

print(fake.email())

print(fake.free_email())

print(fake.free_email_domain())

print(fake.hostname())

print(fake.http_method()) # http请求方法

print(fake.iana_id()) # IANA注册ID

print(fake.ipv4()) # 随机ip

print(fake.ipv4_network_class()) # 网络类别

print(fake.ipv4_private())

print(fake.ipv4_public())

print(fake.ipv6())

print(fake.mac_address()) # mac地址

print(fake.nic_handle()) # 网卡处理ID

print(fake.nic_handles())

print(fake.port_number()) # 端口号

print(fake.ripe_id()) # 组织ID

print(fake.safe_domain_name()) # 域名

print(fake.safe_email()) # 邮箱

print(fake.slug()) # Django算法

print(fake.tld()) # 域名后缀

print(fake.uri()) # http请求路径

print(fake.uri_extension())

print(fake.uri_page()) # 请求页面名

print(fake.uri_path()) # 资源路径

print(fake.url()) # url

print(fake.user_name()) # 用户名


# 61、isbn规则相关

print(fake.isbn10())

print(fake.isbn13())


# 62、工作的职位名称

print(fake.job())


# 63、文章相关

print(fake.paragraph(nb_sentences=5)) # 生成段落

print(fake.paragraph(nb_sentences=5, variable_nb_sentences=False))

print(fake.paragraph(nb_sentences=5, ext_word_list=['abc', 'def', 'ghi', 'jkl']))

print(fake.paragraph(nb_sentences=5, variable_nb_sentences=False, ext_word_list=['abc', 'def', 'ghi', 'jkl']))

print(fake.paragraphs(nb=5)) # 生成段落list

print(fake.sentence(nb_words=10)) # 生成一个句子

print(fake.sentence(nb_words=10, variable_nb_words=False))

print(fake.sentences()) # 生成句子list

print(fake.sentences(nb=5))

print(fake.text(max_nb_chars=20)) # 文本字符串

print(fake.text(max_nb_chars=80))

print(fake.text(max_nb_chars=160))

print(fake.text(ext_word_list=['abc', 'def', 'ghi', 'jkl']))

print(fake.texts(nb_texts=5)) # 文本字符串列表

print(fake.texts(nb_texts=5, max_nb_chars=50))

print(fake.texts(nb_texts=5, max_nb_chars=50, ext_word_list=['abc', 'def', 'ghi', 'jkl']))

print(fake.word()) # 词语字符串

print(fake.word(ext_word_list=['abc', 'def', 'ghi', 'jkl']))

print(fake.words()) # 词语列表

print(fake.words(nb=5, ext_word_list=['abc', 'def', 'ghi', 'jkl']))

print(fake.words(nb=4, ext_word_list=['abc', 'def', 'ghi', 'jkl'], unique=True))


# 数据类型相关

print(fake.binary(length=64)) # 创建字节

print(fake.boolean(chance_of_getting_true=75)) # 布尔类型

print(fake.csv(header=('Name', 'Address', 'Favorite Color'), data_columns=('{{name}}', '{{address}}', '{{safe_color_name}}'), num_rows=10, include_row_ids=True)) # 生成随机的逗号分隔值

print(fake.dsv(data_columns=('{{name}}', '{{address}}'), num_rows=5, delimiter='$')) # 生成随机分隔符分隔值。

print(fake.fixed_width(data_columns=[(20, 'name'), (3, 'pyint', {'min_value':50, 'max_value':100})], align='right', num_rows=2)) # 生成随机固定宽度值

print(fake.image(size=(16, 16), hue=[90, 270], image_format='ico')) # 使用Python图像库生成一张图片并在上面绘制一个随机的多边形。如果没有安装它，这个提供程序将无法运行。以给定格式返回表示图像的字节。

print(fake.json(data_columns=[('Name', 'name'), ('Points', 'pyint', {'min_value':50, 'max_value':100})], num_rows=1)) # 生成随机的JSON结构值

print(fake.md5(raw_output=False)) # 生成MD5数据

print(fake.null_boolean()) # 生成空值或布尔值

print(fake.password(length=12)) # 生成密码

print(fake.password(length=40, special_chars=False, upper_case=False))

print(fake.psv(header=('Name', 'Address', 'Favorite Color'), data_columns=('{{name}}', '{{address}}', '{{safe_color_name}}'), num_rows=10, include_row_ids=True)) # 生成随机的管道分隔值

print(fake.sha1(raw_output=False)) # 生成一个随机的SHA1哈希

print(fake.sha256(raw_output=False)) # 生成一个随机的SHA256哈希

print(fake.tar(uncompressed_size=256, num_files=32, min_file_size=4, compression='bz2')) # 生成包含一个随机有效tar文件的字节对象。

print(fake.tsv(header=('Name', 'Address', 'Favorite Color'), data_columns=('{{name}}', '{{address}}', '{{safe_color_name}}'), num_rows=10, include_row_ids=True)) # 生成随机的制表符分隔值

print(fake.uuid4()) # 如果使用可调用对象指定，则生成一个随机UUID4对象并将其转换为另一种类型

print(fake.uuid4(cast_to=None))

print(fake.zip(uncompressed_size=256, num_files=32, min_file_size=4, compression='bz2')) # 生成包含一个随机有效的zip归档文件的bytes对象。


# 人相关

print(fake.first_name()) # 人名

print(fake.first_name_female()) # 女名

print(fake.first_name_male()) # 男名

print(fake.first_name_nonbinary())

print(fake.language_name())

print(fake.last_name())

print(fake.last_name_female())

print(fake.last_name_male())

print(fake.last_name_nonbinary())

print(fake.name())

print(fake.name_female())

print(fake.name_male())

print(fake.name_nonbinary())

print(fake.prefix())

print(fake.prefix_female())

print(fake.prefix_male())

print(fake.prefix_nonbinary())

print(fake.suffix())

print(fake.suffix_female())

print(fake.suffix_male())

print(fake.suffix_nonbinary())


# 电话号码相关

print(fake.country_calling_code()) # 区号

print(fake.msisdn())

print(fake.phone_number())


# 个人信息相关

print(fake.profile())

print(fake.simple_profile())


# python相关（python数据类型）

print(fake.pybool())

print(fake.pydecimal())

print(fake.pydict())

print(fake.pyfloat())

print(fake.pyint())

print(fake.pyiterable())

print(fake.pylist())

print(fake.pyset())

print(fake.pystr())

print(fake.pystr_format())

print(fake.pystruct())

print(fake.pytuple())


# ssn

print(fake.ssn()) # 865-50-6891


# 默认用户代理相关、认证信息相关、通行证相关

print(fake.android_platform_token())

print(fake.chrome())

print(fake.firefox())

print(fake.internet_explorer())

print(fake.ios_platform_token())

print(fake.linux_platform_token())

print(fake.linux_processor())

print(fake.mac_platform_token())

print(fake.mac_processor())

print(fake.opera())

print(fake.safari())

print(fake.user_agent())

print(fake.windows_platform_token())