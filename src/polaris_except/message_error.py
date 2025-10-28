# -*- coding: utf-8 -*-
"""
descr: 消息推送异常
auther: lj.michale
create_date: 2025/9/19 17:11
file_name: message_error.py
"""

class MessageError(Exception):
    """
    消息推送异常
    """
    
class MessageClientError(MessageError):
    """
    消息客户端推送异常
    """

