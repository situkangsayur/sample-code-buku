"""Kode 4.5: repeat-until di Python dengan while True dan break (Algoritma 4.5)."""


def banyak_digit(n: int) -> int:
    d = 0
    while True:
        n = n // 10
        d = d + 1
        if n == 0:          # syarat until, tidak dibalik
            break
    return d


def jumlah_digit(n: int) -> int:
    """Coba Sendiri di Subbab 4.5."""
    t = 0
    while True:
        t = t + n % 10
        n = n // 10
        if n == 0:
            break
    return t


if __name__ == "__main__":
    assert banyak_digit(2026) == 4
    assert banyak_digit(0) == 1
    assert banyak_digit(9) == 1
    assert banyak_digit(10) == 2
    assert all(banyak_digit(n) == len(str(n)) for n in range(5000))
    assert jumlah_digit(2026) == 10
    assert jumlah_digit(0) == 0
    print("repeat_until.py: semua uji lolos")
