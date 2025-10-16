# -*- coding: utf-8 -*-

"""
descr: 数仓质检
auther: lj.michale
create_date: 2025/9/27 15:54
file_name: kw_dw_quality_inspect.py
"""

import pandas as pd
import requests
from impala.dbapi import connect
import configparser


def config_read_ini():
    db_host_o="10.53.0.71"
    db_port_o=21050
    db_user_o="root"
    db_pass_o=""
    db_base_o="impala"
    db_ini = [db_host_o,db_port_o,db_user_o,db_pass_o,db_base_o]

    return db_ini

def sql_impala_read(sql):
    """
    读取bi_data 任务配置文件
    :param sql:
    :return:
    """
    cursor = connect(host=impala_ini[0],
                     port=impala_ini[1],
                     user=impala_ini[2],
                     password=impala_ini[3],
                     database=impala_ini[4]).cursor()
    cursor.execute(sql)
    res_list = cursor.fetchall()
    cursor.close()

    return res_list

def send_weixin(content):
    """
    微信消息发送
    :param content:
    :return:
    """
    # 这里就是群机器人的Webhook地址
    url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=0ab2779c-220c-425a-8144-5c37b39b5b82"
    headers = {"Content-Type": "application/json"} # http数据头，类型为json
    data = {
        "msgtype": "text",
        "text": {
            "content": content,
            "mentioned_list": [],
        }
    }
    requests.post(url, headers=headers, json=data)


if __name__ == '__main__':
    print(" >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> start !")
    impala_ini = config_read_ini()
    sql_impala_read("show databases")
    print(impala_ini)
    print(sql_impala_read("select * from bi_data.dws_oe_order_ds limit 10"))
    send_weixin("微信消息测试")
    meta_sql = f''' select id
                          ,check_type
                          ,table_name
                          ,check_sql
                          ,remark
                          ,threshold_min
                          ,threshold_max
                          ,create_time
                          ,last_update_time 
                     from   bi_ods.dask_dw_quality_check_meta   
                    '''
    meta_list = sql_impala_read(meta_sql)
    for i in range(len(meta_list)):
        subset = meta_list[i]
        print(subset)




    print(" >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> end !")