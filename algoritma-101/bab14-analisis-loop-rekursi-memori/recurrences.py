"""Bab 14: menghitung kerja fungsi rekursif dan mencocokkannya dengan rekurensi."""
import sys


def factorial(n, counter):
    counter[0] += 1                   # satu pemanggilan = satu satuan kerja
    if n <= 1:
        return 1
    return n * factorial(n - 1, counter)   # T(n) = T(n-1) + c


def bsearch(a, x, lo, hi, counter):
    counter[0] += 1
    if lo > hi:
        return -1
    mid = (lo + hi) // 2
    if a[mid] == x:
        return mid
    if a[mid] < x:
        return bsearch(a, x, mid + 1, hi, counter)
    return bsearch(a, x, lo, mid - 1, counter)  # T(n) = T(n/2) + c


def split_work(n):
    """Kerja T(n) = 2T(n/2) + n dengan T(1) = 1 (n pangkat dua)."""
    if n == 1:
        return 1
    return 2 * split_work(n // 2) + n


def fib_calls(n):
    """Banyak pemanggilan fib naif: C(n) = C(n-1) + C(n-2) + 1."""
    if n <= 1:
        return 1
    return fib_calls(n - 1) + fib_calls(n - 2) + 1


def main():
    c = [0]
    assert factorial(10, c) == 3628800 and c[0] == 10

    a = list(range(1024))
    c = [0]
    bsearch(a, -5, 0, len(a) - 1, c)
    print("binary search gagal pada n=1024:", c[0], "pemanggilan")   # 11
    assert c[0] == 11

    for k in range(0, 11):
        n = 2 ** k
        assert split_work(n) == n * k + n           # n log2 n + n
    print("T(1024) =", split_work(1024))            # 11264

    calls = [fib_calls(n) for n in range(0, 21, 5)]
    print("pemanggilan fib(0,5,10,15,20):", calls)  # [1, 15, 177, 1973, 21891]
    assert calls == [1, 15, 177, 1973, 21891]

    print("batas rekursi Python di mesin ini:", sys.getrecursionlimit())
    print("semua uji lolos")


if __name__ == "__main__":
    main()
