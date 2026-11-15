"""Bab 21: batas bawah sorting berbasis perbandingan.

1. Untuk n kecil, cari banyak perbandingan TERBANYAK (worst case) merge sort
   dan insertion sort atas semua n! permutasi, lalu bandingkan dengan
   batas bawah ceil(log2 n!).
2. Hitung perbandingan yang dilakukan sorted() bawaan Python pada data
   terurut, terbalik, dan acak.
"""
import math
import random
from functools import cmp_to_key
from itertools import permutations


def merge_sort_count(a):
    """Merge sort top-down; mengembalikan (hasil, banyak perbandingan)."""
    if len(a) <= 1:
        return list(a), 0
    mid = len(a) // 2
    left, cl = merge_sort_count(a[:mid])
    right, cr = merge_sort_count(a[mid:])
    out, i, j, c = [], 0, 0, cl + cr
    while i < len(left) and j < len(right):
        c += 1
        if left[i] <= right[j]:
            out.append(left[i]); i += 1
        else:
            out.append(right[j]); j += 1
    out.extend(left[i:]); out.extend(right[j:])
    return out, c


def insertion_sort_count(a):
    a = list(a)
    c = 0
    for i in range(1, len(a)):
        key, j = a[i], i - 1
        while j >= 0:
            c += 1
            if a[j] > key:
                a[j + 1] = a[j]; j -= 1
            else:
                break
        a[j + 1] = key
    return a, c


def lower_bound(n):
    return math.ceil(math.log2(math.factorial(n))) if n > 1 else 0


def worst_over_perms(sorter, n):
    worst = 0
    for p in permutations(range(n)):
        out, c = sorter(p)
        assert out == list(range(n))
        worst = max(worst, c)
    return worst


def count_builtin(data):
    counter = [0]

    def cmp(x, y):
        counter[0] += 1
        return (x > y) - (x < y)

    out = sorted(data, key=cmp_to_key(cmp))
    assert out == sorted(data)
    return counter[0]


if __name__ == "__main__":
    print(" n      n!  ceil(log2 n!)  merge(worst)  insertion(worst)")
    for n in range(1, 9):
        lb = lower_bound(n)
        wm = worst_over_perms(merge_sort_count, n)
        wi = worst_over_perms(insertion_sort_count, n)
        assert lb <= wm <= wi
        assert wi == n * (n - 1) // 2
        print(f"{n:>2} {math.factorial(n):>7} {lb:>14} {wm:>13} {wi:>17}")

    n = 1000
    rng = random.Random(20)
    data = list(range(n))
    shuffled = data[:]
    rng.shuffle(shuffled)
    c_sorted = count_builtin(data)
    c_rev = count_builtin(data[::-1])
    c_rand = count_builtin(shuffled)
    assert c_sorted == n - 1 and c_rev == n - 1
    assert c_rand >= lower_bound(n)
    print(f"sorted() n={n}: terurut {c_sorted}, terbalik {c_rev}, acak {c_rand}, "
          f"ceil(log2 n!) = {lower_bound(n)}")
    print("sort_lower_bound.py: semua uji lolos")
