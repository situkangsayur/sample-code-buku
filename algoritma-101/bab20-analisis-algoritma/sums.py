"""Bab 20: deret untuk loop bersarang yang tidak seragam.

Setiap fungsi menghitung banyak iterasi terdalam, lalu dicocokkan dengan rumus
deret di buku (Tabel 20.2) dan dengan batas atas/bawahnya.
"""
import math


def divisor_counts(n):
    """Algoritma 20.1: d[j] = banyak pembagi j, untuk j = 1..n.

    Loop dalam melompat j = i, 2i, 3i, ... sehingga berputar floor(n/i) kali.
    """
    d = [0] * (n + 1)          # indeks 0 tidak dipakai, sama dengan pseudocode
    steps = 0
    for i in range(1, n + 1):
        for j in range(i, n + 1, i):
            d[j] += 1
            steps += 1
    return d, steps


def squares_loop(n):
    """for i = 1..n: for j = 1..i*i -> jumlah i^2."""
    steps = 0
    for i in range(1, n + 1):
        for _ in range(i * i):
            steps += 1
    return steps


def doubling_loop(n):
    """for i = 1..n: j = 1; while j <= i: j = 2j -> jumlah (floor(log2 i) + 1)."""
    steps = 0
    for i in range(1, n + 1):
        j = 1
        while j <= i:
            j *= 2
            steps += 1
    return steps


def harmonic(n):
    return sum(1.0 / k for k in range(1, n + 1))


def log2_factorial(n):
    return sum(math.log2(k) for k in range(1, n + 1))


if __name__ == "__main__":
    d, steps = divisor_counts(6)
    assert d[1:] == [1, 2, 2, 3, 2, 4]
    assert steps == 14 == sum(6 // i for i in range(1, 7))

    for n in [10, 100, 1000, 10**5]:
        _, s = divisor_counts(n)
        assert s == sum(n // i for i in range(1, n + 1))
        h = harmonic(n)
        # batas dari integral: ln(n+1) <= H_n <= 1 + ln n
        assert math.log(n + 1) <= h <= 1 + math.log(n)
        # n*H_n - n < s <= n*H_n karena floor(n/i) > n/i - 1
        assert n * h - n < s <= n * h
        print(f"divisor n={n:>6}: langkah={s:>8}  n*H_n={n*h:11.1f}  n ln n={n*math.log(n):11.1f}")

    for n in [1, 5, 10, 50]:
        assert squares_loop(n) == n * (n + 1) * (2 * n + 1) // 6

    for n in [1, 2, 8, 100, 1000]:
        s = doubling_loop(n)
        assert s == sum(i.bit_length() for i in range(1, n + 1))
        # batas atas: setiap suku <= log2 n + 1
        assert s <= n * (math.log2(n) + 1)
        # batas bawah: separuh atas, setiap suku >= log2(n/2)
        if n >= 2:
            assert s >= (n / 2) * math.log2(n / 2)
        print(f"doubling n={n:>5}: langkah={s:>6}  n(log2 n + 1)={n*(math.log2(n)+1):9.1f}")

    for n in [4, 8, 16, 100, 1000]:
        lf = log2_factorial(n)
        assert (n / 2) * math.log2(n / 2) <= lf <= n * math.log2(n)
        print(f"log2 {n}! = {lf:9.2f}   (n/2)log2(n/2) = {(n/2)*math.log2(n/2):9.2f}"
              f"   n log2 n = {n*math.log2(n):9.2f}")
    print("sums.py: semua uji lolos")
