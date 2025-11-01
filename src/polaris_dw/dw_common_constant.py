# -*- coding: utf-8 -*-

"""
descr: 数仓通用常量
auther: lj.michale
create_date: 2025/9/27 15:54
file_name: dw_common_constant.py
"""

# 中英文映射
CN_EN_MAPPING = {
    "营销域":"Marketing",
    "‌供应链域":"Supply",
    "物流域":"Logistics",
    "采购域":"Purchase",
    "库存域":"Inventory",
    "制造域":"Manufacture",
    "商品域":"Product",
    "用户域":"User",
    "管理域":"Manage",
    "人资域":"Human Resources"
}

# 英文与简写映射
EN_ABBRE_MAPPING = {
    "Marketing":"Marketing",
    "Supply":"Supply",
    "Logistics":"Logistics",
    "Purchase":"Purchase",
    "Inventory":"Inventory",
    "Manufacture":"Manufacture",
    "Product":"Product",
    "User":"User",
    "Manage":"Manage",
    "Human Resources":"HR"
}

# 数仓通用数据域(中文)
DW_DATA_DOMAIN_CN = {
    '营销域': {
        "销售域":{"客服域":"","交易域":"","用户域":"","商品域":""},
        "运营域":{"客服域":"","会员域":"","交易域":"","促销域":"","售后域":"","价格域":"","用户域":"","商品域":""}
    },
    '‌供应链域': {
        "物流域":{"快递域":"","运单域":""},
        "采购域":"",
        "库存域":""
    },
    '制造域': {
        "设备域":"",
        "质量域":""
    },
    '商品域': "",
    '用户域': {"属性域":"","行为域":""},
    '管理域': {
        "人资域":"",
        "流程域":"",
        "财务域":""
    },
    '基础域': {
        "作业域":"",
        "服务域":"",
        "数据域":""
    }
}

# 数仓通用数据域(英文)
DW_DATA_DOMAIN_EN = {

}