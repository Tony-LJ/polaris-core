# -*- coding: utf-8 -*-

"""
descr: 数仓质检
auther: lj.michale
create_date: 2025/9/27 15:54
file_name: kw_dw_quality_inspect.py
"""
import re
from polaris_message.massage_push_bot import WechatBot
from polaris_kw import send_dw_quality_markdown_msg
from datetime import datetime
from impala.dbapi import connect
from polaris_connector.mysql import MysqlClient


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

def match_check_type(pattern, s):
    """
     匹配
    :param pattern:
    :param s:
    :return:
    """
    return re.search(pattern, s)

if __name__ == '__main__':
    print(" >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> start !")
    mysql_client = MysqlClient(
        host='10.53.0.71',
        database='bigdata',
        user='root',
        password='LJkwhadoop2025!',
        port=3306
    )
    # webhook_url = "https://work.weixin.qq.com/wework_admin/common/openBotProfile/24ecfe4b4e965b4fa53c23bf699d09c849"
    webhook_url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=f318a3b2-383b-451c-bef3-e637c8df4b07"
    msg_rebot = WechatBot(webhook_url)
    now = datetime.now()
    current_date = now.strftime('%Y-%m-%d %H:%M:%S')
    impala_ini = config_read_ini()
    # ############# 查询风控规则库
    meta_sql = f''' select id
                          ,check_type
                          ,table_name
                          ,check_sql
                          ,remark
                          ,threshold_min
                          ,threshold_max
                          ,DATE_FORMAT(create_time, '%Y-%m-%d') as create_time
                          ,DATE_FORMAT(last_update_time, '%Y-%m-%d') as last_update_time
                          ,is_holidays_sensitive
                          ,importance
                          ,creator
                     from bigdata.dw_quality_check_rules '''
    meta_sql2 = f''' select id
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
                     from bi_ods.dw_quality_check_rules_v1 '''
    meta_list = mysql_client.query(meta_sql)

    quality_error_lst = []   # 错误检测结果收集列表
    error_list = []
    important_error_list = []
    wanzhengxing_results = []
    yizhixing_results = []
    zhujianweiyi_results = []
    zhunquexing_results = []

    for i in range(len(meta_list)):
        rule_record = meta_list[i]

        id = rule_record["id"]
        check_type = rule_record["check_type"]
        table_name = rule_record["table_name"]
        check_sql = rule_record["check_sql"]
        threshold_min = rule_record["threshold_min"]
        threshold_max = rule_record["threshold_max"]
        importance = rule_record["importance"]
        is_holidays_sensitive = rule_record["is_holidays_sensitive"]
        creator = rule_record["creator"]
        print("数仓风控规则:{},检查类型:{},表名:{},具体检测规则:{},最小阀值:{},最大阀值:{},重要性:{}".format(i,check_type,table_name,check_sql,threshold_min,threshold_max,importance))

        if check_type == "完整性":
            meta_cnt = sql_impala_read(check_sql)
            if meta_cnt[0][0] == 0:
                result_set = ['error',table_name,id,meta_cnt[0][0],check_type]
                quality_error_lst.append(result_set)
                print("【完整性】 => 数仓风控规则:{},检查类型:{},表名:{},具体检测规则:{}".format(i,check_type,table_name,check_sql))
                error_list.append("{}{}检查规则异常 ".format(table_name,check_type))
                wanzhengxing_results.append(table_name)

        elif check_type == "主键唯一":
            meta_cnt = sql_impala_read(check_sql)
            if meta_cnt[0][0] > 0:
                result_set = ['error',table_name,id,meta_cnt[0][0],check_type]
                quality_error_lst.append(result_set)
                print("【主键唯一】 => 数仓风控规则:{},检查类型:{},表名:{},具体检测规则:{}".format(i,check_type,table_name,check_sql))
                error_list.append("{}{}检查规则异常 ".format(table_name,check_type))
                zhujianweiyi_results.append(table_name)

        elif check_type == "一致性":
            meta_cnt = sql_impala_read(check_sql)
            if meta_cnt[0][0] > 0:
                result_set = ['error',table_name,id,meta_cnt[0][0],check_type]
                quality_error_lst.append(result_set)
                print("【一致性】 => 数仓风控规则:{},检查类型:{},表名:{},具体检测规则:{}".format(i,check_type,table_name,check_sql))
                error_list.append("{}{}检查规则异常 ".format(table_name,check_type))
                yizhixing_results.append(table_name)

        elif check_type == "准确性":
            meta_cnt = sql_impala_read(check_sql)
            if(meta_cnt[0][0] is not None):
                ss = meta_cnt[0]
                if meta_cnt[0][0] < threshold_min:
                    result_set = ['error',table_name,id,meta_cnt[0][0],check_type]
                    quality_error_lst.append(result_set)
                    print("【准确性】 => 数仓风控规则:{},检查类型:{},表名:{},具体检测规则:{}".format(i,check_type,table_name,check_sql))
                    error_list.append("{}{}检查规则异常 ".format(table_name,check_type))
                    zhunquexing_results.append(table_name)
                elif meta_cnt[0][0] > threshold_max:
                    result_set = ['error',table_name,id,meta_cnt[0][0],check_type]
                    quality_error_lst.append(result_set)
                    print("【准确性】 => 数仓风控规则:{},检查类型:{},表名:{},具体检测规则:{}".format(i,check_type,table_name,check_sql))
                    error_list.append("{}{}检查规则异常 ".format(table_name,check_type))
                    zhunquexing_results.append(table_name)
                else:
                    print(f'''质量检测任务成功==>任务id={id}==>表名={table_name}''')
            else:
                result_set = ['error',table_name,id,meta_cnt[0][0],check_type]
                quality_error_lst.append(result_set)
                print("【准确性】 => 数仓风控规则:{},检查类型:{},表名:{},具体检测规则:{}".format(i,check_type,table_name,check_sql))
                error_list.append("{}{}检查规则异常 ".format(table_name,check_type))
                zhunquexing_results.append(table_name)

    # ############# 数仓质检评估规则
    if len(quality_error_lst) == 0:
        print(f'''质量检测任务完成==>任务数{len(meta_list)}==>得分{len(meta_list)}''')
    else:
        print(f'''质量检测任务完成==>任务数{len(meta_list)}==>得分{len(meta_list)-len(quality_error_lst)}''')
        for result_set in quality_error_lst:
            print(f'''{result_set[2]}任务失败:{result_set[1]} 检查 {result_set[4]} 报错!''')

    # ############# 生成每日质检报告
    report_content = send_dw_quality_markdown_msg(current_date,
                                                  meta_list,
                                                  quality_error_lst,
                                                  important_error_list,
                                                  wanzhengxing_results, yizhixing_results, zhujianweiyi_results, zhunquexing_results)
    # msg_rebot.send_markdown(content=report_content)
    print(" >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> end !")

    # TODO:
    #  1.巡检报告中新增巡检人员栏目
    #  2.质检异常简易修复(还未提)



