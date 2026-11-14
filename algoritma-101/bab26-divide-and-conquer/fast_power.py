"""Pangkat cepat."""


def fast_power(a, n, m=None):
    """Menghitung a^n (mod m bila m diberikan) dengan O(log n) perkalian."""
    if n == 0:
        return 1 if m is None else 1 % m
    half = fast_power(a, n // 2, m)          # satu panggilan, dipakai dua kali
    hasil = half * half
    if n % 2 == 1:
        hasil = hasil * a
    return hasil if m is None else hasil % m


def multiplications(n):
    """Banyak perkalian yang dilakukan fast_power untuk eksponen n."""
    if n == 0:
        return 0
    return multiplications(n // 2) + 1 + (n % 2)


if __name__ == "__main__":
    print(fast_power(3, 13))                 # 1594323
    assert fast_power(3, 13) == 3 ** 13
    assert fast_power(2, 10) == 1024
    assert fast_power(7, 0) == 1
    assert fast_power(2, 100, 1_000_000_007) == pow(2, 100, 1_000_000_007)
    for a in range(-5, 6):
        for n in range(0, 40):
            assert fast_power(a, n) == a ** n
    print("perkalian untuk n=13:", multiplications(13))   # 7
    assert multiplications(13) == 7
    print("semua uji pangkat cepat lolos")
