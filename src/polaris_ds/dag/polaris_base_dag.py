# -*- coding: utf-8 -*-

"""
descr: 自定义基础DAG结构
auther: lj.michale
create_date: 2025/10/27 15:54
file_name: polaris_base_dag.py
"""
from polaris_ds.dag.polaris_edge import PolarisEdge
from polaris_ds.dag.polaris_node import PolarisNode
import networkx as nx


class PolarisBaseDAG:
    def __init__(self):
        self.G = nx.DiGraph()  # 使用有向图来表示DAG
        self.nodes = {}  # Dictionary to hold nodes by name
        self.edges = []  # List of tuples (dependency, node)

    # def add_node(self, node):
    #     """
    #     添加一个节点到图中
    #     :param node:
    #     :return:
    #     """
    #     self.G.add_node(node)
    def add_node(self, node):
        if node.node_id not in self.nodes:
            self.nodes[node.node_id] = node
        else:
            raise ValueError(f"Node {node.node_id} already exists.")

    def add_edge(self, edge):
        """
        添加一条边到图中
        :param edge:
        :return:
        """
        self.G.add_edge(edge.start, edge.end)

    def execute(self):
        visited = set()  # To keep track of visited nodes to handle cycles gracefully
        for node in self.nodes.values():
            if node not in visited:
                self._dfs(node, visited)


    def _dfs(self, node, visited):
        if node in visited:  # Cycle detected, skip this node to avoid infinite loop
            return
        visited.add(node)
        node.execute()  # Execute the node's logic here
        for dependency in node.dependencies:  # Ensure dependencies are executed first
            if dependency not in visited:
                self._dfs(dependency, visited)

    def print_structure(self):
        """
        打印DAG的结构
        :return:
        """
        print("Nodes:")
        for node in self.G.nodes():
            print(node.__dict__)
        print("\nEdges:")
        for edge in self.G.edges():
            print(f"From {edge[0].__dict__} to {edge[1].__dict__}")


if __name__ == '__main__':
    # 创建节点和边实例
    node1 = PolarisNode('1-1',1, 1)
    node2 = PolarisNode('2-1',2, 1)
    node3 = PolarisNode('3-1',3, 1)
    node4 = PolarisNode('4-1',4, 1)
    edge1 = PolarisEdge(node1, node2)
    edge2 = PolarisEdge(node2, node3)
    edge3 = PolarisEdge(node3, node4)

    # 创建DAG实例并添加节点和边
    dag = PolarisBaseDAG()
    dag.add_node(node1)
    dag.add_node(node2)
    dag.add_node(node3)
    dag.add_node(node4)

    dag.add_edge(edge1)
    dag.add_edge(edge2)
    dag.add_edge(edge3)

    # 打印DAG结构
    dag.print_structure()
    dag.execute()
