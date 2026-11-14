"""Bab 9: list, function, dan module.

Jalankan: python3 list_dan_fungsi.py
"""
import math
from statistics import mean


def rata_rata(a):
    """Rata-rata list a; mengembalikan None bila a kosong."""
    if len(a) == 0:
        return None
    total = 0
    for x in a:                      # for-each: tanpa indeks
        total += x
    return total / len(a)


def tambah_nol(a):
    """Mengubah list a di tempat: list dikirim sebagai referensi."""
    a.append(0)


def ganti(a):
    """Mengganti nama a di dalam fungsi tidak mengubah list pemanggil."""
    a = [99]
    return a


def jarak(x1, y1, x2=0.0, y2=0.0):
    """Parameter dengan nilai bawaan."""
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


if __name__ == "__main__":
    nilai = [70, 85, 90, 65]
    assert nilai[0] == 70 and nilai[-1] == 65      # indeks negatif dari belakang
    assert nilai[1:3] == [85, 90]                  # slice: indeks 1 dan 2
    assert len(nilai) == 4
    assert rata_rata(nilai) == 77.5
    assert rata_rata([]) is None
    assert rata_rata(nilai) == mean(nilai)

    nilai.append(100)
    assert nilai == [70, 85, 90, 65, 100]
    nilai.insert(0, 50)                            # sisip di depan: semua elemen bergeser
    assert nilai[0] == 50 and len(nilai) == 6

    b = nilai                                      # b dan nilai menunjuk list yang sama
    b[0] = 1
    assert nilai[0] == 1
    c = nilai.copy()                               # salinan terpisah
    c[0] = 2
    assert nilai[0] == 1

    x = [1, 2]
    tambah_nol(x)
    assert x == [1, 2, 0]
    y = ganti(x)
    assert x == [1, 2, 0] and y == [99]

    # list 2D: hati-hati dengan [[0] * 3] * 2
    salah = [[0] * 3] * 2
    salah[0][0] = 5
    assert salah[1][0] == 5                        # baris kedua ikut berubah
    benar = [[0] * 3 for _ in range(2)]
    benar[0][0] = 5
    assert benar[1][0] == 0

    assert jarak(3, 4) == 5.0
    assert jarak(1, 1, 4, 5) == 5.0
    kuadrat = [i * i for i in range(1, 6)]         # list comprehension
    assert kuadrat == [1, 4, 9, 16, 25]
    print("nilai =", nilai)
    print("Semua uji list_dan_fungsi.py lolos.")
