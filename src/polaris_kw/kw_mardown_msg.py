# -*- coding: utf-8 -*-

"""
descr: 数仓质检
auther: lj.michale
create_date: 2025/9/27 15:54
file_name: kw_mardown_msg.py
"""

def send_dw_quality_markdown_msg(current_date,
                                 meta_list,
                                 quality_error_list,
                                 important_error_list,
                                 wanzhengxing_list,
                                 yizhixing_list,
                                 zhujianweiyi_list,
                                 zhunquexing_list,
                                 error_cause_dict):
    """
    发送数仓质检markdown报告
    :param current_date:
    :param meta_list:
    :param quality_error_list:
    :param important_error_list:
    :param wanzhengxing_list:
    :param yizhixing_list:
    :param zhujianweiyi_list:
    :param zhunquexing_list:
    :param error_cause_dict:
    :return:
    """
    report_content = f'''# **每日数仓质检报告**
                         > **质检日期**: <font color='black'> {current_date} </font> 
                         > **质检人**: <font color='black'> 大数据团队 </font>
                         > **质检规则库**: <font color='black'> bi_ods.dw_quality_check_rules </font>
                         > **质检规则数**: <font color='black'> {len(meta_list)} </font>
                         > **质检异常数**: <font color='red'> {len(quality_error_list)} </font> 
                         > **质检得分**: <font color='green'> {round(((len(meta_list)-len(quality_error_list))/len(meta_list)) * 100, 2)} </font> 
                         > **质检重要异常列表**: <font color='black'> {important_error_list} </font> 
                         > **质检全部异常列表**: <font color='black'> 完整性异常:{wanzhengxing_list},\n 一致性异常:{yizhixing_list},\n 主键唯一异常:{zhujianweiyi_list},\n 准确性异常:{zhunquexing_list} </font> 
                         > **质检异常原因列表**: <font color='black'> 完整性异常原因:{wanzhengxing_list},\n 一致性异常原因:{yizhixing_list},\n 主键唯一异常原因:{zhujianweiyi_list},\n 准确性异常原因:{zhunquexing_list} </font> 
    '''

    return report_content


