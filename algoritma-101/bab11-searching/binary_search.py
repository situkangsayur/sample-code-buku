"""Bab 11: binary search.

Jalankan: python3 binary_search.py
"""
import bisect
import random


def binary_search(a, x):
    """Indeks i dengan a[i] == x pada list terurut a, atau -1."""
    lo, hi = 0, len(a) - 1           # pseudocode: lo <- 1, hi <- n
    while lo <= hi:
        mid = lo + (hi - lo) // 2    # sama dengan (lo + hi) // 2, aman di bahasa lain
        if a[mid] == x:
            return mid
        elif a[mid] < x:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1


def binary_search_jejak(a, x):
    """Binary search yang mencatat (lo, hi, mid, a[mid]) di setiap putaran."""
    jejak = []
    lo, hi = 0, len(a) - 1
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        jejak.append((lo, hi, mid, a[mid]))
        if a[mid] == x:
            return mid, jejak
        elif a[mid] < x:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1, jejak


def lower_bound(a, x):
    """Indeks pertama i dengan a[i] >= x (len(a) bila tidak ada)."""
    lo, hi = 0, len(a)               # ruang [lo, hi) setengah terbuka
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if a[mid] < x:
            lo = mid + 1
        else:
            hi = mid
    return lo


if __name__ == "__main__":
    a = [3, 8, 15, 21, 27, 34, 42, 50, 61, 77]
    assert binary_search(a, 42) == 6
    assert binary_search(a, 3) == 0 and binary_search(a, 77) == 9
    assert binary_search(a, 20) == -1
    assert binary_search(a, 1) == -1 and binary_search(a, 100) == -1
    assert binary_search([], 5) == -1
    assert binary_search([5], 5) == 0 and binary_search([5], 4) == -1

    idx, jejak = binary_search_jejak(a, 42)
    for baris in jejak:
        print("lo=%d hi=%d mid=%d a[mid]=%d" % baris)
    assert jejak == [(0, 9, 4, 27), (5, 9, 7, 50), (5, 6, 5, 34), (6, 6, 6, 42)]
    _, jejak20 = binary_search_jejak(a, 20)
    assert jejak20 == [(0, 9, 4, 27), (0, 3, 1, 8), (2, 3, 2, 15), (3, 3, 3, 21)]

    assert lower_bound(a, 20) == 3 and lower_bound(a, 21) == 3
    assert lower_bound(a, 100) == 10 and lower_bound(a, 0) == 0

    # uji acak: bandingkan dengan modul bisect bawaan
    rng = random.Random(2026)
    for _ in range(2000):
        n = rng.randint(0, 40)
        b = sorted(rng.sample(range(200), n))     # tanpa duplikat
        x = rng.randint(-5, 205)
        i = binary_search(b, x)
        if x in b:
            assert b[i] == x
        else:
            assert i == -1
        assert lower_bound(b, x) == bisect.bisect_left(b, x)
    print("Semua uji binary_search.py lolos.")
