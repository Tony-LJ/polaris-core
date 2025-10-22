# -*- coding: utf-8 -*-

"""
descr: 封装二叉树
auther: lj.michale
create_date: 2025/10/27 15:54
file_name: binary_tree.py
"""

class BinaryTree(object):
    def __init__(self, root):
        self.root = root

    def pre_travel(self, root):
        """前序遍历: 根左右"""
        if (root != None):
            print(root.val, end = ',')
            self.pre_travel(root.left)
            self.pre_travel(root.right)


    def in_travel(self, root):
        """中序遍历: 左根右"""
        if (root != None):
            self.in_travel(root.left)
            print(root.val, end = ',')
            self.in_travel(root.right)

    def last_travel(self, root):
        """后序遍历: 左右根"""
        if (root != None):
            self.last_travel(root.left)
            self.last_travel(root.right)
            print(root.val, end = ',')
