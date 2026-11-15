"""Bab 35: pertumbuhan list Python dan analisis amortized.

Bagian 1 mengamati kapasitas list CPython lewat sys.getsizeof.
Bagian 2 menghitung biaya salin pada tiga strategi pertumbuhan.
Rumus CPython 3.12 (Objects/listobject.c, fungsi list_resize):
    new_allocated = (newsize + (newsize >> 3) + 6) & ~3
"""
import platform
import sys


def kapasitas_teramati(n):
    """Daftar (panjang saat kapasitas berubah, kapasitas baru)."""
    a, hasil, terakhir = [], [], None
    dasar = sys.getsizeof([])
    for i in range(n):
        a.append(i)
        kap = (sys.getsizeof(a) - dasar) // 8   # 8 byte per pointer (64-bit)
        if kap != terakhir:
            hasil.append((len(a), kap))
            terakhir = kap
    return hasil


def rumus_cpython(newsize):
    return (newsize + (newsize >> 3) + 6) & ~3


def kapasitas_rumus(n):
    hasil, kap = [], 0
    for panjang in range(1, n + 1):
        if panjang > kap:
            kap = rumus_cpython(panjang)
            hasil.append((panjang, kap))
    return hasil


def biaya_salin(n, tumbuh):
    """Jumlah elemen yang disalin saat n kali append dengan aturan tumbuh."""
    kap, salin = 0, 0
    for panjang in range(1, n + 1):
        if panjang > kap:
            salin += panjang - 1      # pindahkan isi lama ke blok baru
            kap = tumbuh(kap, panjang)
    return salin


def dobel(kap, perlu):
    return max(2 * kap, perlu, 4)


def tambah_tetap(kap, perlu):
    return kap + 4


if __name__ == "__main__":
    teramati = kapasitas_teramati(70)
    print("kapasitas teramati:", teramati)
    cpython = platform.python_implementation() == "CPython"
    if cpython and sys.maxsize > 2**32 and sys.version_info[:2] >= (3, 9):
        assert teramati == kapasitas_rumus(70)
        assert [k for _, k in teramati][:6] == [4, 8, 16, 24, 32, 40]

    n = 1_000_000
    s_dobel = biaya_salin(n, dobel)
    s_cpy = biaya_salin(n, lambda kap, p: rumus_cpython(p))
    s_tetap = biaya_salin(10_000, tambah_tetap)
    print("dobel      : %d salinan untuk %d append (%.2f per append)" % (s_dobel, n, s_dobel / n))
    print("CPython    : %d salinan untuk %d append (%.2f per append)" % (s_cpy, n, s_cpy / n))
    print("tambah +4  : %d salinan untuk 10000 append" % s_tetap)
    assert s_dobel <= 2 * n                 # amortized O(1)
    assert s_cpy <= 10 * n                  # faktor 1,125: konstanta lebih besar
    assert s_tetap > 10_000 * 10_000 // 10  # kuadratik
    print("pertumbuhan_list: semua uji lolos")
