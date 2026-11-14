"""Kode 5.1: JumlahPositif (Algoritma 5.3), Gambar 5.4(b) dan 5.6.
Deretan bilangan diberikan sebagai list yang diakhiri 0, bukan dibaca dari keyboard."""


def jumlah_positif(deret: list[int]) -> int:
    total = 0
    k = 0
    x = deret[k]                 # priming read
    while x != 0:
        if x > 0:
            total = total + x
        k = k + 1
        x = deret[k]             # baca x berikutnya
    return total


def jumlah_positif_kusut(deret: list[int]) -> int:
    """Terjemahan langsung Gambar 5.4(a): dua garis balik menjadi continue, keluar di tengah."""
    total = 0
    k = 0
    while True:
        x = deret[k]
        k = k + 1
        if x == 0:
            break
        if x < 0:
            continue
        total = total + x
    return total


if __name__ == "__main__":
    for deret, h in [([5, -3, 4, 0], 9), ([0], 0), ([-1, -2, 0], 0), ([7, 0, 99], 7)]:
        assert jumlah_positif(deret) == h
        assert jumlah_positif_kusut(deret) == h
    try:
        jumlah_positif([1, 2])   # tidak diakhiri 0: melanggar prasyarat
    except IndexError:
        pass
    else:
        raise AssertionError("seharusnya IndexError")
    print("jumlah_positif.py: semua uji lolos")
