"""Uji prima Miller-Rabin, algoritma Monte Carlo (Algoritma 33.1, Kode 33.2)."""
import random


def miller_rabin(n, k=20, rng=random):
    if n < 2:
        return False
    for p in (2, 3, 5, 7, 11, 13):
        if n % p == 0:
            return n == p
    # tulis n - 1 = 2^s * d dengan d ganjil
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for _ in range(k):
        a = rng.randrange(2, n - 1)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False          # a adalah saksi: n pasti komposit
    return True                   # mungkin prima, salah dengan peluang <= 4^-k


def prima_naif(n):
    if n < 2:
        return False
    i = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += 1
    return True


if __name__ == "__main__":
    rng = random.Random(2026)
    print(miller_rabin(561, rng=rng))          # False (bilangan Carmichael)
    print(miller_rabin(2 ** 61 - 1, rng=rng))  # True (prima Mersenne)
    print(miller_rabin(2 ** 61 + 1, rng=rng))  # False
    for n in range(0, 5000):
        assert miller_rabin(n, rng=rng) == prima_naif(n)
    assert pow(2, 560, 561) == 1   # 561 menipu uji Fermat basis 2
    print("semua uji lolos")
