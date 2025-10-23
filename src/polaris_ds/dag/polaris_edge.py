# -*- coding: utf-8 -*-

"""
descr: 树节点
auther: lj.michale
create_date: 2025/10/27 15:54
file_name: polaris_node.py
"""
class PolarisEdge(object):
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __repr__(self):
        return f"Edge(from={self.start}, to={self.end})"