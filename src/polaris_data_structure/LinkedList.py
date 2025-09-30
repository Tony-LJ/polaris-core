# -*- coding: utf-8 -*-

"""
descr : 链表
auther : lj.michale
create_date : 2025/9/27 15:54
file_name : LinkedList.py
"""

from polaris_data_structure.ListNode import ListNode


class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, value):
        if not self.head:
            self.head = ListNode(value)
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = ListNode(value)

    def delete(self, value):
        current = self.head
        prev = None
        while current and current.value != value:
            prev = current
            current = current.next
        if prev is None:  # 要删除的是头节点
            self.head = current.next if current else None
        elif current:  # 要删除的是非头节点
            prev.next = current.next

    def print_list(self):
        current = self.head
        while current:
            print(current.value, end=" -> ")
            current = current.next
        print("None")
