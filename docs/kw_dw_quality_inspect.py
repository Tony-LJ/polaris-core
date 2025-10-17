# -*- coding: utf-8 -*-

"""
descr: 数仓质检
auther: lj.michale
create_date: 2025/9/27 15:54
file_name: kw_dw_quality_inspect.py
"""

from polaris_message.massage_push_bot import WechatBot
from datetime import datetime
import pandas as pd
import requests
from fontTools.merge.util import current_time
from impala.dbapi import connect
import configparser
import json


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


if __name__ == '__main__':
    print(" >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> start !")
    webhook_url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=34f51e63-9ab5-43fa-8621-377b7bf70064"
    msg_rebot = WechatBot(webhook_url)
    now = datetime.now()
    current_date = now.strftime('%Y-%m-%d %H:%M:%S')
    impala_ini = config_read_ini()
    # 查询风控规则库
    meta_sql = f''' select id
                          ,check_type
                          ,table_name
                          ,check_sql
                          ,remark
                          ,threshold_min
                          ,threshold_max
                          ,create_time
                          ,last_update_time
                          ,creator
                          ,importance 
                     from bi_ods.dw_quality_check_rules '''
    meta_list = sql_impala_read(meta_sql)

    quality_error_lst = []   # 错误检测结果收集列表
    error_list = []

    for i in range(len(meta_list)):
        subset = meta_list[i]
        # id 表名，检测代码，上下限阈值
        id,check_type,table_name,check_sql,threshold_min,threshold_max,importance = subset[0],subset[1],subset[2],subset[3],subset[5],subset[6],subset[9]
        print("数仓风控规则:{},检查类型:{},表名:{},具体检测规则:{},最小阀值:{},最大阀值:{},重要性:{}".format(i,check_type,table_name,check_sql,threshold_min,threshold_max,importance))
        meta_cnt = sql_impala_read(check_sql)
        # 如果检测结果 >0 ,则收集检测结果
        if meta_cnt[0][0] is None:
            result_set = ['error',table_name,id,meta_cnt[0][0],check_type]
            quality_error_lst.append(result_set)
            print("【=None情况】 => 数仓风控规则:{},检查类型:{},表名:{},具体检测规则:{}".format(i,check_type,table_name,check_sql))
            error_list.append("=None规则:{}".format(check_sql))
        elif meta_cnt[0][0] < threshold_min:
            result_set = ['error',table_name,id,meta_cnt[0][0],check_type]
            quality_error_lst.append(result_set)
            print("【<最小阀值情况】 => 数仓风控规则:{},检查类型:{},表名:{},具体检测规则:{},最小阀值:{}".format(i,check_type,table_name,check_sql,threshold_min))
            error_list.append("<最小阀值规则:{}".format(check_sql))
        elif meta_cnt[0][0] > threshold_max:
            result_set = ['error',table_name,id,meta_cnt[0][0],check_type]
            quality_error_lst.append(result_set)
            print("【>最大阀值情况】 => 数仓风控规则:{},检查类型:{},表名:{},具体检测规则:{},最大阀值:{}".format(i,check_type,table_name,check_sql,threshold_max))
            error_list.append(">最大阀值规则:{}".format(check_sql))
        else:
            print(f'''质量检测任务成功==>任务id={id}==>表名={table_name}''')

    # 数仓质检评估规则
    if len(quality_error_lst) == 0:
        print(f'''质量检测任务完成==>任务数{len(meta_list)}==>得分{len(meta_list)}''')
    else:
        print(f'''质量检测任务完成==>任务数{len(meta_list)}==>得分{len(meta_list)-len(quality_error_lst)}''')
        for result_set in quality_error_lst:
            print(f'''{result_set[2]}任务失败:{result_set[1]} 检查 {result_set[4]} 报错!''')

    # 生成每日质检报告
    report_content = f'''# **每日数仓质检报告**\n
                         > **质检日期**: <font color='black'> {current_date} </font> \n
                         > **质检人**: <font color='black'> 大数据团队 </font> \n
                         > **质检规则库**: <font color='black'> bi_ods.dask_dw_quality_check_meta </font> \n
                         > **质检异常数**: <font color='red'> {len(quality_error_lst)} </font> \n
                         > **质检得分**: <font color='green'> {round(((len(meta_list)-len(quality_error_lst))/len(meta_list)) * 100, 2)} </font> \n
                         > **质检异常详细列表**: <font color='black'> {error_list} </font> \n     
    '''
    msg_rebot.send_markdown(content=report_content)
    print(" >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> end !")



