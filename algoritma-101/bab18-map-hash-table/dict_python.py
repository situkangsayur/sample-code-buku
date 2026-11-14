"""dict Python: polynomial hash, hitung kata, hash bawaan (Algoritma 18.1, Kode 18.4, Subbab 18.5).

Diuji dengan CPython 3.12.
"""
import sys


def hash_polinomial(s, m, b=31):
    """h(s) = (s0*b^(L-1) + s1*b^(L-2) + ... + s(L-1)) mod m, dihitung cara Horner."""
    h = 0
    for c in s:
        h = (h * b + ord(c)) % m
    return h


def hitung_kata(teks):
    frek = {}
    for kata in teks.lower().split():
        frek[kata] = frek.get(kata, 0) + 1
    return frek


if __name__ == "__main__":
    # contoh tangan PolyHash di Subbab 18.2: "abc" dengan b = 31, m = 11
    # ((97*31 + 98)*31 + 99) mod 11
    assert hash_polinomial("abc", 11) == ((97 * 31 + 98) * 31 + 99) % 11 == 5
    assert hash_polinomial("ab", 11) != hash_polinomial("ba", 11)

    frek = hitung_kata("data masuk data keluar data hilang masuk")
    assert frek == {"data": 3, "masuk": 2, "keluar": 1, "hilang": 1}
    # urutan sisip dijamin sejak Python 3.7
    assert list(frek) == ["data", "masuk", "keluar", "hilang"]

    # hash bilangan bulat kecil adalah bilangan itu sendiri, kecuali -1
    assert hash(5) == 5 and hash(-1) == -2
    # hash str diacak per proses (lihat PYTHONHASHSEED)
    print("algoritma hash str:", sys.hash_info.algorithm)
    # kunci harus hashable: list tidak boleh, tuple boleh
    d = {(1, 2): "tuple boleh"}
    try:
        d[[1, 2]] = "list"
        raise AssertionError("seharusnya TypeError")
    except TypeError:
        pass
    print("dict_python.py: semua uji lolos")
