# -*- coding: utf-8 -*-

"""
descr: 基础DAG结构
auther: lj.michale
create_date: 2025/10/27 15:54
file_name: base_dag.py
"""

import networkx as nx

class BaseDAG:
    def __init__(self):
        self.graph = nx.DiGraph()

    def add_node(self, node):
        """
        添加一个节点到图中
        :param node:
        :return:
        """
        if node not in self.graph:
            self.graph.add_node(node)
        else:
            raise ValueError(f"Node {node} already exists in the graph.")

    def add_edge(self, from_node, to_node):
        """
        添加一个边到图中
        :param from_node:
        :param to_node:
        :return:
        """
        if from_node not in self.graph:
            raise ValueError(f"From node {from_node} does not exist in the graph.")
        if to_node not in self.graph:
            raise ValueError(f"To node {to_node} does not exist in the graph.")
        self.graph.add_edge(from_node, to_node)

    def remove_node(self, node):
        """
        从图中移除一个节点
        :param node:
        :return:
        """
        if node in self.graph:
            self.graph.remove_node(node)
        else:
            raise ValueError(f"Node {node} does not exist in the graph.")

    def remove_edge(self, from_node, to_node):
        """
        从图中移除一个边
        :param from_node:
        :param to_node:
        :return:
        """
        if self.graph.has_edge(from_node, to_node):
            self.graph.remove_edge(from_node, to_node)
        else:
            raise ValueError(f"Edge ({from_node}, {to_node}) does not exist in the graph.")

    def topological_sort(self):
        """
        返回图的拓扑排序
        :return:
        """
        try:
            return list(nx.topological_sort(self.graph))
        except nx.NetworkXUnfeasible:
            raise ValueError("The graph has at least one cycle and cannot be topologically sorted.")

    def is_acyclic(self):
        """
        检查图是否为无环的
        :return:
        """
        return nx.is_directed_acyclic_graph(self.graph)
