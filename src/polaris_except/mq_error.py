# -*- coding: utf-8 -*-
"""
descr: MQ消息推送异常
auther: lj.michale
create_date: 2025/9/19 17:11
file_name: mq_error.py
"""

class MqError(Exception):
    """
    MQ消息推送异常
    """
    
class MessageClientError(MqError):
    """
    MQ消息客户端推送异常
    """

