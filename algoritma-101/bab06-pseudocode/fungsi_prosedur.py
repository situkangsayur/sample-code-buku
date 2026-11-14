"""Kode 6.1: procedure Tukar dan function CariMaks (Algoritma 6.2, 6.3), ditambah
HitungMuncul (Algoritma 6.1), RataRata, dan Balik. Indeks Python mulai dari 0."""


def tukar(a: list[int], i: int, j: int) -> None:
    temp = a[i]
    a[i] = a[j]
    a[j] = temp              # list pemanggil ikut berubah


def cari_maks(a: list[int]) -> int:
    maks = a[0]              # A[1] di pseudocode
    for i in range(1, len(a)):   # i = 2..n di pseudocode
        if a[i] > maks:
            maks = a[i]
    return maks


def hitung_muncul(a: list[int], x: int, k: int) -> int:
    c = 0
    for v in a:
        if not (v == x):
            continue         # bukan x, lewati
        c = c + 1
        if c == k:
            break            # batas tercapai
    return c


def jumlah_array(a: list[float]) -> float:
    total = 0
    for v in a:
        total = total + v
    return total


def rata_rata(a: list[float]) -> float:
    return jumlah_array(a) / len(a)


def balik(a: list[int]) -> None:
    """Latihan 7: membalik di tempat dengan Tukar. A[i] <-> A[n-i+1] menjadi a[i] <-> a[n-1-i]."""
    n = len(a)
    for i in range(n // 2):
        tukar(a, i, n - 1 - i)


def tambah(x: int) -> None:
    """Latihan 8: x adalah salinan, pemanggil tidak berubah."""
    x = x + 1


if __name__ == "__main__":
    data = [42, 17, 88, 63, 25]
    assert cari_maks(data) == 88
    tukar(data, 0, 2)
    print(data)                  # [88, 17, 42, 63, 25]
    assert data == [88, 17, 42, 63, 25]
    print(cari_maks(data))       # 88
    assert hitung_muncul([3, 1, 3, 3, 2, 3], 3, 2) == 2
    assert hitung_muncul([3, 3, 3, 3], 3, 3) == 3
    assert hitung_muncul([1, 2], 3, 5) == 0
    nilai = [42, 17, 88, 63, 25]
    assert jumlah_array(nilai) == 235 and rata_rata(nilai) == 47
    assert cari_maks(nilai) - rata_rata(nilai) == 41
    for n in range(10):
        b = list(range(n))
        balik(b)
        assert b == list(range(n))[::-1]
    a = 5
    tambah(a)
    assert a == 5
    assert cari_maks([-5, -2, -9]) == -2     # aman untuk bilangan negatif
    print("fungsi_prosedur.py: semua uji lolos")
