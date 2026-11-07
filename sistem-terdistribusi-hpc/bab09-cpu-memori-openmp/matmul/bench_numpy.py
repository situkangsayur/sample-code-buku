"""Versi 6 tabel praktikum: pembanding BLAS lewat NumPy."""
import sys
import time

import numpy as np

n = int(sys.argv[1]) if len(sys.argv) > 1 else 2048
A, B = np.random.rand(n, n), np.random.rand(n, n)
A @ B                                  # pemanasan
t0 = time.perf_counter()
A @ B
t = time.perf_counter() - t0
print(f"6,{n},blas,{t:.3f},{2 * n**3 / t / 1e9:.2f}")
