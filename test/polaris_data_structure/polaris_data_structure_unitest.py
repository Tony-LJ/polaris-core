# -*- coding: utf-8 -*-
from polaris_data_structure.LinkedList import LinkedList


if __name__ == '__main__':
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    ll.append(3)
    ll.print_list()  # 输出: 1 -> 2 -> 3 -> None
    ll.delete(2)
    ll.print_list()  # 输出: 1 -> 3 -> None