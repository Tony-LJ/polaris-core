# -*- coding: utf-8 -*-

"""
descr: 通用队列类
auther: lj.michale
create_date: 2025/10/27 15:54
file_name: base_queue.py
"""

from collections import deque

class BaseQueue:
    def __init__(self):
        """初始化空队列，用deque存储元素"""
        self._items = deque()  # 下划线表示“私有属性”，避免外部直接修改

    def is_empty(self):
        """判断队列是否为空"""
        return len(self._items) == 0

    def enqueue(self, item):
        """入队：在队尾添加元素"""
        self._items.append(item)  # deque.append()：队尾添加，O(1)

    def dequeue(self):
        """出队：从队头移除并返回元素，空队列时抛异常"""
        if self.is_empty():
            raise IndexError("无法出队：队列为空")
        return self._items.popleft()  # deque.popleft()：队头删除，O(1)

    def front(self):
        """查看队头元素，空队列时抛异常"""
        if self.is_empty():
            raise IndexError("无法查看队头：队列为空")
        return self._items[0]  # 直接访问队头元素，O(1)

    def size(self):
        """返回队列中元素的个数"""
        return len(self._items)

    def __str__(self):
        """自定义打印格式，方便调试"""
        return f"Queue([{', '.join(map(str, self._items))}])"


