"""Kode 9.21: menghitung pi dengan Numba prange.
NUMBA_NUM_THREADS=4 python pi_numba.py
"""
import time

from numba import njit, prange


@njit(parallel=True, fastmath=True)
def hitung_pi(n):
    h = 1.0 / n
    s = 0.0
    for i in prange(n):
        x = (i + 0.5) * h
        s += 4.0 / (1.0 + x * x)
    return s * h


print(hitung_pi(10))                 # panggilan pertama: kompilasi (pemanasan)
t0 = time.perf_counter()
print(hitung_pi(1_000_000_000))
print(f"{time.perf_counter() - t0:.3f} s")
