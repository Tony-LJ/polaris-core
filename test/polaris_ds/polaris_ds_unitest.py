# -*- coding: utf-8 -*-

from polaris_ds.queue.base_queue import BaseQueue
from polaris_ds.queue.bounded_queue import BoundedQueue


# 测试队列功能
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