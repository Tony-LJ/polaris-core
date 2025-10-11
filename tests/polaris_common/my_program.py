# -*- coding: utf-8 -*-
import random
import multiprocessing
import time
from multiprocessing.dummy import Process
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

def my_task(x):
    # 模拟耗时操作
    time.sleep(1)
    return x * x

def run_in_threads_with_progress(func, tasks, max_workers=4):
    results = [None] * len(tasks)
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_idx = {
            executor.submit(func, *args): idx
            for idx, args in enumerate(tasks)
        }
        for future in tqdm(as_completed(future_to_idx), total=len(tasks), desc="进度"):
            idx = future_to_idx[future]
            try:
                results[idx] = future.result()
            except Exception as e:
                results[idx] = f"❌ 任务 {idx} 出错 → {e}"
    return results

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
    num_arr = [random.randint(100, 10000) for _ in range(2000)]

    p1 = Process(target=get_prime_arr, args=(num_arr,))
    p2 = Process(target=get_prime_arr, args=(num_arr,))
    p3 = Process(target=get_prime_arr, args=(num_arr,))

    p1.start()
    p2.start()
    p3.start()

    p1.join()
    p2.join()
    p3.join()

