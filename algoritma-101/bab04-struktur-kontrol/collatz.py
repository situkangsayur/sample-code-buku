"""Algoritma 4.4 LangkahCollatz (while) dan 4.3 JumlahSampai (for)."""


def langkah_collatz(n: int) -> int:
    langkah = 0
    while n != 1:
        if n % 2 == 0:
            n = n // 2
        else:
            n = 3 * n + 1
        langkah = langkah + 1
    return langkah


def jumlah_sampai(n: int) -> int:
    total = 0
    for i in range(1, n + 1):   # i = 1..n di pseudocode
        total = total + i
    return total


if __name__ == "__main__":
    assert langkah_collatz(1) == 0
    assert langkah_collatz(6) == 8
    assert langkah_collatz(7) == 16
    assert jumlah_sampai(0) == 0
    assert jumlah_sampai(4) == 10
    assert all(jumlah_sampai(n) == n * (n + 1) // 2 for n in range(100))
    print("collatz.py: semua uji lolos")
