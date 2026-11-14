"""Bab 20: analisis kasus rata-rata dengan random variable indikator.

Untuk n kecil, rata-rata dihitung TEPAT atas semua n! permutasi (pecahan),
lalu dicocokkan dengan rumus di buku:
  - banyak inversi (= banyak geseran insertion sort): n(n-1)/4
  - banyak pembaruan maksimum saat memindai: H_n = 1 + 1/2 + ... + 1/n
"""
from fractions import Fraction
from itertools import permutations


def insertion_sort_shifts(a):
    """Insertion sort (Bab 12) yang menghitung geseran elemen."""
    a = list(a)
    shifts = 0
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]
            shifts += 1
            j -= 1
        a[j + 1] = key
    return shifts


def inversions(a):
    n = len(a)
    return sum(1 for i in range(n) for j in range(i + 1, n) if a[i] > a[j])


def max_updates(a):
    """Algoritma 20.2: banyak kali maksimum sementara diganti (elemen pertama dihitung)."""
    best = None
    updates = 0
    for x in a:
        if best is None or x > best:
            best = x
            updates += 1
    return updates


def harmonic_exact(n):
    return sum(Fraction(1, k) for k in range(1, n + 1))


def exact_averages(n):
    perms = list(permutations(range(1, n + 1)))
    total_shift = total_upd = 0
    for p in perms:
        s = insertion_sort_shifts(p)
        assert s == inversions(p)
        total_shift += s
        total_upd += max_updates(p)
    return Fraction(total_shift, len(perms)), Fraction(total_upd, len(perms))


if __name__ == "__main__":
    print(" n  rata-rata geseran  n(n-1)/4  rata-rata pembaruan max   H_n")
    for n in range(1, 9):
        avg_shift, avg_upd = exact_averages(n)
        assert avg_shift == Fraction(n * (n - 1), 4)
        assert avg_upd == harmonic_exact(n)
        print(f"{n:>2} {str(avg_shift):>18} {n*(n-1)/4:>9} {str(avg_upd):>24} {float(avg_upd):6.4f}")
    assert insertion_sort_shifts([3, 1, 4, 2]) == 3
    assert max_updates([3, 1, 4, 2]) == 2
    print("average_case.py: semua uji lolos")
