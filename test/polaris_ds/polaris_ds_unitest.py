# -*- coding: utf-8 -*-
from polaris_ds.dag import BaseDAG, WeightedDAG
from polaris_ds.queue.base_queue import BaseQueue
from polaris_ds.queue.bounded_queue import BoundedQueue
from polaris_ds.stack.base_stack import BaseStack
from polaris_ds.tree.binary_tree import BinaryTree
from polaris_ds.tree.node import Node


if __name__ == "__main__":
    q = BaseQueue()
    # 测试入队
    q.enqueue("任务1")
    q.enqueue("任务2")
    q.enqueue("任务3")
    print("入队后队列：", q)  # 输出：Queue([任务1, 任务2, 任务3])

    # 测试查看队头和大小
    print("队头元素：", q.front())  # 输出：任务1
    print("队列大小：", q.size())   # 输出：3

    # 测试出队
    print("出队元素：", q.dequeue())  # 输出：任务1
    print("出队后队列：", q)          # 输出：Queue([任务2, 任务3])

    # 测试判空
    print("队列是否为空：", q.is_empty())  # 输出：False

    # 清空队列
    q.dequeue()
    q.dequeue()
    print("清空后队列是否为空：", q.is_empty())  # 输出：True

    # ############### 测试有界队列
    bq = BoundedQueue(max_size=2)

    bq.enqueue("A")
    bq.enqueue("B")
    print("有界队列（容量2）：", bq)  # 输出：Queue([A, B])

    # 尝试添加第3个元素，触发异常
    try:
        bq.enqueue("C")
    except OverflowError as e:
        print("入队异常：", e)  # 输出：入队异常：无法入队：队列已达最大容量

    # ########################栈
    stack = BaseStack()
    stack.push(1)
    stack.push(2)
    stack.push(3)  #入栈三个元素
    print(len(stack))  # 3
    stack.pop()
    print(stack.is_empty()) # False
    print(stack.top())  # 2

    # ########################树结构
    node1 = Node(1)
    node2 = Node(2)
    node3 = Node(3)
    node4 = Node(4)
    node5 = Node(5)
    node6 = Node(6)
    node7 = Node(7)
    node8 = Node(8)
    node9 = Node(9)
    node10 = Node(10)  #生成10个独立的节点

    bt = BinaryTree(root=node1)
    node1.left = node2
    node1.right = node3
    node2.left = node4
    node2.right= node5
    node3.left = node6
    node3.right = node7
    node4.left = node8
    node4.right = node9
    node5.left = node10  # 建立该二叉树的节点关系
    bt.pre_travel(node1)
    print('前序遍历')
    bt.in_travel(node1)
    print('中序遍历')
    bt.last_travel(node1)
    print('后序遍历')

    # ############################### DAG
    # 创建 DAG 实例
    dag = BaseDAG()

    # 添加节点和边
    dag.add_node('A')
    dag.add_node('B')
    dag.add_node('C')
    dag.add_edge('A', 'B')
    dag.add_edge('B', 'C')
    dag.add_edge('A', 'C')  # 这条边会导致图不是无环的，实际操作中应避免添加这样的边。

    # 检查是否为无环图（应为False）并打印结果（实际操作中应避免添加导致循环的边）
    print("Is DAG acyclic?", dag.is_acyclic())  # 应该返回False，因为我们尝试添加了一个导致循环的边。
    print("Topological Sort:", dag.topological_sort())  # 这将抛出异常，因为图中有环。

    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    dag2 = WeightedDAG()
    dag2.add_node('A', 1, 2)
    dag2.add_node('B', 3, 4)
    dag2.add_edge('A', 'B', 5)  # 从A到B的权重为5
    print(dag2.get_edge_weight('A', 'B'))  # 输出边的权重
    print(dag2.shortest_path('A', 'B'))  # 输出从A到B的最短路径（如果有的话）
