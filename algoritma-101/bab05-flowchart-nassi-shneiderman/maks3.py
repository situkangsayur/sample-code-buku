"""Algoritma 5.1 Maks3 (Gambar 5.2), rata-rata n nilai (Gambar 5.3),
dan Algoritma 5.2 Potongan (Tabel keputusan di Subbab 5.2)."""


def maks3(a, b, c):
    if a >= b:
        m = a
    else:
        m = b
    if c > m:
        m = c
    return m


def rata_rata(nilai: list[float]) -> float:
    """Gambar 5.3 dengan nilai dari list; n = len(nilai) >= 1."""
    n = len(nilai)
    total = 0
    i = 1
    while i <= n:
        x = nilai[i - 1]         # indeks Python mulai dari 0
        total = total + x
        i = i + 1
    return total / n


def potongan(anggota: bool, b: int, promosi: bool) -> int:
    if b > 500_000 and promosi:
        return 15
    elif anggota and b > 500_000:
        return 10
    elif anggota:
        return 5
    else:
        return 0                 # asumsi untuk baris keenam tabel keputusan


if __name__ == "__main__":
    assert maks3(4, 9, 7) == 9
    assert maks3(5, 5, 5) == 5
    assert maks3(9, 4, 9) == 9
    assert maks3(2, 7, 11) == 11
    import itertools
    for t in itertools.product(range(-2, 3), repeat=3):
        assert maks3(*t) == max(t)
    assert rata_rata([80, 65, 92]) == 79
    # delapan baris tabel keputusan: (anggota, besar, promosi) -> potongan
    tabel = {(True, True, True): 15, (True, True, False): 10, (True, False, True): 5,
             (True, False, False): 5, (False, True, True): 15, (False, True, False): 0,
             (False, False, True): 0, (False, False, False): 0}
    for (ang, besar, promo), h in tabel.items():
        b = 600_000 if besar else 200_000
        assert potongan(ang, b, promo) == h
    print("maks3.py: semua uji lolos")
