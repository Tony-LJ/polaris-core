# -*- coding: utf-8 -*-

"""
descr: 爬虫相关工具
auther: lj.michale
create_date: 2025/9/27 15:54
file_name: crawler_utils.py
"""

def get_browser_headers(referer="https://image.baidu.com/"):
    """
    获取模拟浏览器的请求头，适配百度图片反爬策略，支持自定义Referer
    :param referer:  referer (str): 请求头中的Referer字段，默认指向百度图片首页，
                      若爬取其他平台可修改（如搜狗图片：https://image.sogou.com/）
    :return:  dict: 符合浏览器请求规范的Headers字典
    """
    return {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Connection": "keep-alive",
        "Referer": referer
    }
