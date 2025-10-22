# -*- coding: utf-8 -*-

"""
descr: 带权重的DAG结构
auther: lj.michale
create_date: 2025/10/27 15:54
file_name: weight_dag.py
"""
import networkx as nx

class WeightedDAG:
    def __init__(self):
        self.graph = nx.DiGraph()  # 使用DiGraph来确保是有向无环图

    def add_node(self, node_id, x, y):
        """ 添加一个节点到图中，节点带有x-y坐标 """
        if node_id not in self.graph:
            self.graph.add_node(node_id, pos=(x, y))
        else:
            print(f"Node {node_id} already exists.")

    def add_edge(self, from_node, to_node, weight):
        """ 添加一个带权重的边，确保不会形成环 """
        try:
            nx.add_path(self.graph, [from_node, to_node])  # 尝试添加路径，这将自动处理权重
            # 设置边的权重，如果需要的话（networkx通常会自动处理权重）
            self.graph[from_node][to_node]['weight'] = weight
        except nx.NetworkXUnfeasible:
            print(f"Adding edge from {from_node} to {to_node} would create a cycle.")

    def get_node_position(self, node_id):
        """ 获取节点的x-y坐标 """
        return self.graph.nodes[node_id].get('pos', None)

    def get_edge_weight(self, from_node, to_node):
        """ 获取边的权重 """
        return self.graph[from_node][to_node].get('weight', None)

    def shortest_path(self, source, target):
        """ 计算从源节点到目标节点的最短路径 """
        try:
            path = nx.shortest_path(self.graph, source, target, weight='weight')
            return path
        except nx.NetworkXNoPath:
            print("No path exists between the nodes.")
            return None


