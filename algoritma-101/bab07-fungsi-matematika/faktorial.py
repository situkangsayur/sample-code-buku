"""Algoritma 7.1 Faktorial (iteratif), notasi Sigma/Pi sebagai loop, dan deret (Subbab 7.2-7.3)."""
import math


def faktorial(n: int) -> int:
    hasil = 1                    # perkalian kosong bernilai 1
    for i in range(2, n + 1):
        hasil = hasil * i
    return hasil


def sigma(a, awal: int, akhir: int):
    """Jumlah a(i) untuk i dari awal sampai akhir; 0 bila tidak ada suku."""
    total = 0
    for i in range(awal, akhir + 1):
        total = total + a(i)
    return total


def pi(a, awal: int, akhir: int):
    """Hasil kali a(i) untuk i dari awal sampai akhir; 1 bila tidak ada suku."""
    hasil = 1
    for i in range(awal, akhir + 1):
        hasil = hasil * a(i)
    return hasil


def prefix_sum(a: list[int]) -> list[int]:
    """Contoh di Subbab 7.5: n-1 penjumlahan, bukan n(n+1)/2."""
    p = [0] * len(a)
    if a:
        p[0] = a[0]
    for k in range(1, len(a)):
        p[k] = p[k - 1] + a[k]
    return p


if __name__ == "__main__":
    assert faktorial(0) == 1 and faktorial(1) == 1 and faktorial(5) == 120
    assert faktorial(20) == 2_432_902_008_176_640_000
    assert faktorial(21) == math.factorial(21) == 51_090_942_171_709_440_000
    assert faktorial(21) > 2**64 - 1 > faktorial(20)      # 21! tidak muat di u64
    assert sigma(lambda i: i * i, 1, 4) == 30
    assert sigma(lambda i: i, 1, 0) == 0
    assert pi(lambda i: i, 1, 5) == 120 and pi(lambda i: i, 1, 0) == 1
    for n in range(50):
        assert sigma(lambda i: i, 1, n) == n * (n + 1) // 2
        assert sigma(lambda i: i * i, 1, n) == n * (n + 1) * (2 * n + 1) // 6
        assert sigma(lambda k: 2**k, 0, n) == 2**(n + 1) - 1
    assert prefix_sum([3, 1, 4, 1, 5]) == [3, 4, 8, 9, 14]
    print("faktorial.py: semua uji lolos")
