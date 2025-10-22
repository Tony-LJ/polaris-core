# -*- coding: utf-8 -*-

"""
descr: 树节点
auther: lj.michale
create_date: 2025/10/27 15:54
file_name: node.py
"""
class Node(object):
    """节点类"""
    def __init__(self, val=None, left=None, right=None):  #生成节点时，要定义左节点和右节点
        self.val = val
        self.left = left
        self.right = right
