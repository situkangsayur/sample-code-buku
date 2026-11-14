"""Bab 14: mengukur waktu O(n) dan O(n^2) di Python. Angka bergantung mesin.

Jalankan: python3 benchmark.py
Setiap ukuran diulang REPEAT kali dan yang dilaporkan median.
"""
import platform
import random
import statistics
import time

REPEAT = 5


def sum_linear(a):
    total = 0
    for v in a:
        total += v
    return total


def count_pairs(a, x):
    n = len(a)
    count = 0
    for i in range(n - 1):
        ai = a[i]
        for j in range(i + 1, n):
            if ai + a[j] == x:
                count += 1
    return count


def median_time(fn, *args):
    times = []
    for _ in range(REPEAT):
        t0 = time.perf_counter()
        fn(*args)
        times.append(time.perf_counter() - t0)
    return statistics.median(times)


def main():
    rng = random.Random(14)
    print("Python", platform.python_version(), platform.processor() or platform.machine())
    for n in [10**5, 10**6, 10**7]:
        a = [rng.randint(1, 1000) for _ in range(n)]
        print(f"O(n)   n={n:>9,d}  {median_time(sum_linear, a):.4f} s")
    for n in [1000, 2000, 4000, 8000]:
        a = [rng.randint(1, 10**6) for _ in range(n)]
        print(f"O(n^2) n={n:>9,d}  {median_time(count_pairs, a, 10**6):.4f} s")
    assert count_pairs([3, 1, 4, 1, 5], 5) == 2
    assert sum_linear([1, 2, 3]) == 6
    print("semua uji lolos")


if __name__ == "__main__":
    main()
