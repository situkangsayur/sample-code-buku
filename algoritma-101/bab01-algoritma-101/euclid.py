"""Bab 1: algoritma Euclid untuk FPB (faktor persekutuan terbesar).

Versi pengurangan (paling dekat dengan Elemen Euclid, Buku VII)
dan versi sisa bagi (bentuk modern).
"""
import math


def fpb_kurang(a, b):
    """Kurangi bilangan yang lebih besar dengan yang lebih kecil sampai sama."""
    assert a > 0 and b > 0
    while a != b:
        if a > b:
            a = a - b
        else:
            b = b - a
    return a


def fpb_sisa(a, b, jejak=None):
    """Ganti (a, b) dengan (b, a mod b) sampai b = 0."""
    while b != 0:
        if jejak is not None:
            jejak.append((a, b, a % b))
        a, b = b, a % b
    return a


if __name__ == "__main__":
    jejak = []
    assert fpb_sisa(1071, 462, jejak) == 21
    for baris in jejak:
        print("a=%5d  b=%5d  a mod b=%5d" % baris)
    # (1071, 462, 147), (462, 147, 21), (147, 21, 0)
    assert jejak == [(1071, 462, 147), (462, 147, 21), (147, 21, 0)]
    assert fpb_kurang(1071, 462) == 21
    for a in range(1, 120):
        for b in range(1, 120):
            assert fpb_sisa(a, b) == fpb_kurang(a, b) == math.gcd(a, b)
    print("semua uji lolos")
