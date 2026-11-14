"""Kode 7.2: Euclid (Algoritma 7.2), dicocokkan dengan math.gcd. Ditambah KPK (Latihan 7)."""
import math


def euclid(a: int, b: int) -> int:
    while b != 0:
        r = a % b          # % adalah mod
        a = b
        b = r
    return a


def euclid_jejak(a: int, b: int) -> list[tuple[int, int]]:
    """Pasangan (a, b) sesudah setiap ulangan, untuk mencocokkan tabel tracing."""
    jejak = [(a, b)]
    while b != 0:
        a, b = b, a % b
        jejak.append((a, b))
    return jejak


def kpk(a: int, b: int) -> int:
    return (a // euclid(a, b)) * b


if __name__ == "__main__":
    assert euclid(252, 105) == 21
    assert euclid(252, 105) == math.gcd(252, 105)
    assert euclid_jejak(252, 105) == [(252, 105), (105, 42), (42, 21), (21, 0)]
    assert euclid_jejak(1071, 462) == [(1071, 462), (462, 147), (147, 21), (21, 0)]
    assert euclid(105, 252) == 21 and len(euclid_jejak(105, 252)) == 5   # satu ulangan tambahan
    assert len(euclid_jejak(55, 34)) - 1 == 8                           # Fibonacci, Bab 8
    for a in range(0, 60):
        for b in range(0, 60):
            if a or b:
                assert euclid(a, b) == math.gcd(a, b)
    assert kpk(4, 6) == 12 and kpk(21, 6) == 42
    assert -7 % 3 == 2      # Python mengikuti tanda pembagi
    print("euclid.py: semua uji lolos")
