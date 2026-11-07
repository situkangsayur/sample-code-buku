"""Kode 8.2: menghitung bilangan prima dengan multiprocessing.
Pemakaian: python prima.py <jumlah_proses> [N]
Keluaran: p,detik,jumlah_prima
"""
import sys
import time
from multiprocessing import Pool


def prima(n):
    if n < 2:
        return False
    d = 2
    while d * d <= n:
        if n % d == 0:
            return False
        d += 1
    return True


def hitung(args):
    awal, n, p = args
    return sum(1 for i in range(awal, n, p) if prima(i))


if __name__ == "__main__":
    p = int(sys.argv[1])
    N = int(sys.argv[2]) if len(sys.argv) > 2 else 2_000_000
    mulai = time.perf_counter()
    with Pool(p) as pool:
        total = sum(pool.map(hitung, [(w, N, p) for w in range(p)]))
    dt = time.perf_counter() - mulai
    print(f"{p},{dt:.4f},{total}")
