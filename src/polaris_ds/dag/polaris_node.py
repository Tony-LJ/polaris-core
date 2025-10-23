# -*- coding: utf-8 -*-

"""
descr: 树节点
auther: lj.michale
create_date: 2025/10/27 15:54
file_name: polaris_node.py
"""
import time

class PolarisNode(object):
    def __init__(self, node_id, x, y):  #生成节点时，要定义左节点和右节点
        self.node_id = node_id
        self.x = x
        self.y = y
        self.start_time = None
        self.end_time = None
        self.edges = []
        self.dependencies = []
        self.execute_func = None

    def add_edge(self, target_node):
        """
        添加一条从当前节点到目标节点的边
        :param target_node:
        :return:
        """
        self.edges.append(target_node)

    def execute(self):
        if self.execute_func:
            self.execute_func()
        self.start_time = time.time()
        print(f"Executing DAG Node:{self.node_id}...")
        # 模拟任务执行，例如：
        time.sleep(1)  # 模拟耗时操作
        self.end_time = time.time()
        print(f"{self.node_id} executed in {self.end_time - self.start_time:.2f} seconds.")
