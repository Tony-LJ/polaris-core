# -*- coding: utf-8 -*-

"""
descr: 树节点
auther: lj.michale
create_date: 2025/10/27 15:54
file_name: polaris_node.py
"""
class PolarisNode(object):
    def __init__(self, node_id, x, y):  #生成节点时，要定义左节点和右节点
        self.node_id = node_id
        self.x = x
        self.y = y
        self.edges = []

    def add_edge(self, target_node):
        """ 添加一条从当前节点到目标节点的边 """
        self.edges.append(target_node)
