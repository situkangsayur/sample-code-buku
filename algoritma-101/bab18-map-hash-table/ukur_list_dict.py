"""Mengukur 'x in list' dan 'x in dict' untuk satu juta kunci (pembuka Bab 18).

Hasil bergantung mesin. Di buku: Python 3.12.3, Intel Xeon E5-2697 v4,
14 November 2026, list sekitar 10 ms dan dict sekitar 78 ns per pencarian
(angka dict termasuk overhead pemanggilan lambda).
"""
import sys
import timeit

if __name__ == "__main__":
    n = 1_000_000
    data = list(range(n))
    d = {k: True for k in data}
    x = n - 1                       # kunci terakhir: kasus terburuk untuk list
    t_list = min(timeit.repeat(lambda: x in data, number=20, repeat=5)) / 20
    t_dict = min(timeit.repeat(lambda: x in d, number=200000, repeat=5)) / 200000
    print("Python", sys.version.split()[0])
    print(f"x in list : {t_list * 1e3:8.2f} ms")
    print(f"x in dict : {t_dict * 1e9:8.1f} ns")
    assert t_dict < t_list
    print("ukur_list_dict.py: selesai")
