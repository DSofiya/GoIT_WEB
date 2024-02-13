import multiprocessing
import time
from functools import partial

def measure_execution_time(func, *args):
    start_time = time.time()
    result = func(*args)
    end_time = time.time()
    execution_time = end_time - start_time
    return result, execution_time

def factorize_number(number):
    factors = []
    for i in range(1, number + 1):
        if number % i == 0:
            factors.append(i)

    return factors

def factorize(*numbers):
    results = []
    for number in numbers:
        factors = factorize_number(number)
        results.append(factors)

    return results

def parallel_factorize_number(number):
    return factorize_number(number)



if __name__ == "__main__":
    numb = [128, 255,99999, 10651060]
    start_time_sync = time.time()
    a, b, c, d = factorize(*numb)
    end_time_sync = time.time()
    sync_time = end_time_sync - start_time_sync
    # assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    # assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    # assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    # assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]

    print("Час синхронних обчислень:", sync_time)
    print(f"Результати синхронних обчислень:{a, b, c, d}")

    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
    partial_func = partial(parallel_factorize_number)
    parallel_results, parallel_time = measure_execution_time(pool.map, partial_func, numb)
    pool.close()
    pool.join()

    print("Час паралельних обчислень:", parallel_time)
    print(f"Результати паралельних обчислень:{parallel_results}")
  
