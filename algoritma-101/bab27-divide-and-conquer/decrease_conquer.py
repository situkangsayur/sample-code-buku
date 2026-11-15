"""Decrease and conquer: tiga variasi."""
import random


def binary_search_rec(a, x, lo, hi):
    """Decrease by a constant factor: ruang dibuang separuh setiap langkah."""
    if lo > hi:
        return -1
    mid = (lo + hi) // 2
    if a[mid] == x:
        return mid
    if a[mid] < x:
        return binary_search_rec(a, x, mid + 1, hi)
    return binary_search_rec(a, x, lo, mid - 1)


def insertion_sort_rec(a, n=None):
    """Decrease by one: urutkan n-1 elemen pertama, lalu sisipkan elemen ke-n."""
    if n is None:
        n = len(a)
    if n <= 1:
        return
    insertion_sort_rec(a, n - 1)
    kunci = a[n - 1]
    j = n - 2
    while j >= 0 and a[j] > kunci:
        a[j + 1] = a[j]
        j -= 1
    a[j + 1] = kunci


def gcd(a, b):
    """Decrease by a variable size: (a, b) -> (b, a mod b)."""
    if b == 0:
        return a
    return gcd(b, a % b)


if __name__ == "__main__":
    a = [3, 8, 15, 21, 34, 55, 70]
    assert binary_search_rec(a, 34, 0, len(a) - 1) == 4
    assert binary_search_rec(a, 4, 0, len(a) - 1) == -1
    b = [5, 2, 9, 1, 7]
    insertion_sort_rec(b)
    assert b == [1, 2, 5, 7, 9]
    for _ in range(200):
        c = [random.randint(0, 99) for _ in range(random.randint(0, 40))]
        d = list(c)
        insertion_sort_rec(d)
        assert d == sorted(c)
    assert gcd(1071, 462) == 21
    print(gcd(1071, 462))                    # 21
    print("semua uji decrease and conquer lolos")
