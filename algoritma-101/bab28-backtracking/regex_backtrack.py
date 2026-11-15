"""Bab 28: mesin regex backtracking pada pola (a+)+$ (Kode 28.6, kotak Di Lapangan).

Waktu kira-kira berlipat dua setiap satu huruf 'a' ditambahkan, karena mesin
mencoba semua cara membagi deretan 'a' ke dalam grup (a+) sebelum menyerah.
Hasil ukur di buku: Python 3.12.3, Intel Xeon E5-2697 v4, 14 November 2026.
"""
import re
import time

PATTERN = re.compile(r"(a+)+$")


def measure(n):
    text = "a" * n + "b"          # huruf terakhir membuat pencocokan gagal
    t0 = time.perf_counter()
    m = PATTERN.match(text)
    return m, time.perf_counter() - t0


if __name__ == "__main__":
    times = []
    for n in (14, 16, 18, 20):
        m, dt = measure(n)
        assert m is None
        times.append(dt)
        print(f"n = {n:2d}: {dt:.4f} detik")
    # dua huruf tambahan membuat waktu kira-kira empat kali lipat
    assert times[-1] > 4 * times[0]
    assert PATTERN.match("a" * 30) is not None   # kasus berhasil tetap cepat
    print("semua uji lolos")
