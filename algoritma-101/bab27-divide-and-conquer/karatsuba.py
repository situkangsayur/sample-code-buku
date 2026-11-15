"""Perkalian Karatsuba."""
import random


def karatsuba(x, y):
    """Perkalian dua bilangan bulat tak negatif dengan tiga perkalian rekursif."""
    if x < 10 or y < 10:                     # kasus basis: satu digit
        return x * y
    m = max(len(str(x)), len(str(y))) // 2
    p = 10 ** m
    a, b = divmod(x, p)                      # x = a*10^m + b
    c, d = divmod(y, p)                      # y = c*10^m + d
    ac = karatsuba(a, c)
    bd = karatsuba(b, d)
    tengah = karatsuba(a + b, c + d) - ac - bd   # = ad + bc
    return ac * p * p + tengah * p + bd


calls = 0


def karatsuba_count(x, y):
    global calls
    calls += 1
    if x < 10 or y < 10:
        return x * y
    m = max(len(str(x)), len(str(y))) // 2
    p = 10 ** m
    a, b = divmod(x, p)
    c, d = divmod(y, p)
    ac = karatsuba_count(a, c)
    bd = karatsuba_count(b, d)
    t = karatsuba_count(a + b, c + d) - ac - bd
    return ac * p * p + t * p + bd


if __name__ == "__main__":
    print(karatsuba(1234, 5678))             # 7006652
    assert karatsuba(1234, 5678) == 7006652
    assert karatsuba(12, 34) == 408
    for _ in range(500):
        x = random.randint(0, 10 ** 40)
        y = random.randint(0, 10 ** 40)
        assert karatsuba(x, y) == x * y
    print("semua uji karatsuba lolos")
