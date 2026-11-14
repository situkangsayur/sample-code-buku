"""Algoritma 7.3 PangkatCepat dan Kode 7.4 pangkat_mod, dicocokkan dengan pow bawaan."""


def pangkat_cepat(a, n: int):
    hasil = 1
    while n > 0:
        if n % 2 == 1:           # bit terendah n bernilai 1
            hasil = hasil * a
        a = a * a
        n = n // 2               # geser ke bit berikutnya
    return hasil


def pangkat_mod(a: int, n: int, m: int) -> int:
    hasil = 1
    a = a % m
    while n > 0:
        if n % 2 == 1:
            hasil = (hasil * a) % m
        a = (a * a) % m
        n = n // 2
    return hasil


def banyak_perkalian(n: int) -> int:
    """Banyak perkalian yang dijalankan PangkatCepat untuk pangkat n."""
    kali = 0
    while n > 0:
        if n % 2 == 1:
            kali += 1
        kali += 1
        n //= 2
    return kali


if __name__ == "__main__":
    assert pangkat_cepat(3, 13) == 1_594_323 == 3**13
    assert pangkat_cepat(2, 10) == 1024 and pangkat_cepat(5, 0) == 1
    assert all(pangkat_cepat(3, n) == 3**n for n in range(200))
    assert banyak_perkalian(1_000_000) == 27        # 20 kuadrat + 7 perkalian ke hasil
    assert pangkat_mod(3, 13, 10**9 + 7) == 3**13
    assert pangkat_mod(7, 10**18, 10**9 + 7) == pow(7, 10**18, 10**9 + 7)
    assert (10**18).bit_length() == 60
    print("pangkat_cepat.py: semua uji lolos")
