"""Bab 20: memeriksa penyelesaian rekurensi dengan menghitung T(n) secara tepat.

Hasil metode substitusi dan recursion tree di buku dicocokkan dengan nilai
yang dihitung langsung dari rekurensinya.
"""
import math
from functools import lru_cache


@lru_cache(maxsize=None)
def t_merge(n):
    """T(n) = 2T(floor(n/2)) + n, T(1) = 1."""
    if n <= 1:
        return 1
    return 2 * t_merge(n // 2) + n


@lru_cache(maxsize=None)
def t_const(n):
    """T(n) = 2T(floor(n/2)) + 1, T(1) = 1: tebakan T(n) <= c n gagal, T(n) <= 2n - 1 berhasil."""
    if n <= 1:
        return 1
    return 2 * t_const(n // 2) + 1


@lru_cache(maxsize=None)
def t_uneven(n):
    """T(n) = T(floor(n/3)) + T(floor(2n/3)) + n, T(n) = 1 untuk n <= 2."""
    if n <= 2:
        return 1
    return t_uneven(n // 3) + t_uneven(2 * n // 3) + n


@lru_cache(maxsize=None)
def t_master(n, a, b, d):
    """T(n) = a T(floor(n/b)) + n^d, T(1) = 1."""
    if n <= 1:
        return 1
    return a * t_master(n // b, a, b, d) + n ** d


if __name__ == "__main__":
    import sys
    sys.setrecursionlimit(10000)

    # Substitusi: T(n) <= n log2 n + n untuk semua n >= 1 (dibuktikan di buku)
    for n in range(1, 5000):
        assert t_merge(n) <= n * math.log2(n) + n + 1e-9
    for k in range(0, 13):          # n pangkat dua: tepat n log2 n + n
        n = 2 ** k
        assert t_merge(n) == n * k + n
    print("t_merge(1024) =", t_merge(1024))

    # Penguatan hipotesis: T(n) = 2T(n/2)+1 memenuhi T(n) <= 2n - 1
    for n in range(1, 5000):
        assert t_const(n) <= 2 * n - 1
    print("t_const(1024) =", t_const(1024), " 2n-1 =", 2 * 1024 - 1)

    # Recursion tree tak seimbang: n log_3 n <= T(n) <= n log_{3/2} n + n
    print(" n        T(n)    n*log_3 n   n*log_1.5 n + n   T/(n log2 n)")
    for n in [10**3, 10**4, 10**5, 10**6]:
        t = t_uneven(n)
        lo = n * math.log(n, 3)
        hi = n * math.log(n, 1.5) + n
        assert lo <= t <= hi
        print(f"{n:>8} {t:>11} {lo:>12.0f} {hi:>16.0f} {t/(n*math.log2(n)):>12.3f}")

    # Teorema master, tiga kasus (n pangkat 4 atau pangkat 2)
    n = 4 ** 8                      # 65536
    print("root dominan  2T(n/2)+n^2 :", t_master(n, 2, 2, 2) / n**2)
    print("seimbang      4T(n/4)+n   :", t_master(n, 4, 4, 1) / (n * math.log(n, 4)))
    print("leaf dominan  4T(n/2)+n   :", t_master(n, 4, 2, 1) / n**2)
    print("recurrences.py: semua uji lolos")
