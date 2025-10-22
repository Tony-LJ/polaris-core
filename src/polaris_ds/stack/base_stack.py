# -*- coding: utf-8 -*-

"""
descr: 基本栈
auther: lj.michale
create_date: 2025/10/27 15:54
file_name: base_stack.py
"""

class BaseStack(object):
    def __init__(self):
        self.stack = []

    def push(self, value):
        """入栈"""
        self.stack.append(value)  #用列表追加模拟入栈的顺序，即列表的第一位表示栈底，最后一位表示栈顶
        print(f"入栈元素为{value}")

    def pop(self):
        """出栈"""
        if self.is_empty():
            raise  Exception("栈为空")
        item = self.stack.pop()   #pop默认删除最后一个元素，即‘栈顶’元素
        print(f"出栈元素为{item}")
        return  item

    def is_empty(self):
        """判断栈是否为空"""
        return  len(self.stack) == 0   #即长度是否为0

    def top(self):
        """返回栈顶元素"""
        if self.is_empty():
            raise  Exception("栈为空")
        return  self.stack[-1]   #即列表‘入栈’时追加的最后一位

    def __len__(self):
        """魔术方法, len(object)自动执行的方法，查看长度"""
        return  len(self.stack)

#  上面为栈的封装部分，下面的部分是实际的演示，为了更好的理解。


