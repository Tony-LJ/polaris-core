# -*- coding: utf-8 -*-

"""
descr: 有界队列（限制最大容量）
auther: lj.michale
create_date: 2025/10/27 15:54
file_name: bounded_queue.py
"""

from collections import deque
from base_queue import BaseQueue

class BoundedQueue(BaseQueue):
    def __init__(self, max_size):
        """
        初始化有界队列，指定最大容量max_size
        :param max_size:
        """
        super().__init__()  # 继承父类Queue的初始化
        self.max_size = max_size  # 队列最大容量

    def enqueue(self, item):
        """
        入队：若队列满则抛异常
        :param item:
        :return:
        """
        if self.size() >= self.max_size:
            raise OverflowError("无法入队：队列已达最大容量")
        super().enqueue(item)  # 调用父类的入队方法


