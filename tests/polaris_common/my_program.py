# -*- coding: utf-8 -*-
import random


def is_prime(n):
    for i in range(2, n):
        if n % i == 0:
            return False
    return True

def get_prime_arr(arr):
    return [is_prime(elem) for elem in arr]


if __name__ == "__main__":
    num_arr = [random.randint(100, 10000) for _ in range(6000)]
    print(get_prime_arr(num_arr))