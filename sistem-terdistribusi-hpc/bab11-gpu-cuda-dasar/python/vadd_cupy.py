"""Penjumlahan vektor dengan CuPy: operasi array dan RawKernel (Kode 11.9).

Pemasangan (CUDA 12.x): pip install cupy-cuda12x
Jalankan: python vadd_cupy.py
"""
import time

import cupy as cp
import numpy as np

n = 1 << 24
a = cp.ones(n, dtype=cp.float32)          # langsung dibuat di memori GPU
b = cp.full(n, 2.0, dtype=cp.float32)
c = a + b                                 # kernel elementwise bawaan CuPy

tambah = cp.RawKernel(r'''
extern "C" __global__ void tambah(const float *a, const float *b, float *c, int n) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i < n) c[i] = a[i] + b[i];
}''', "tambah")
c2 = cp.empty_like(a)
tambah(((n + 255) // 256,), (256,), (a, b, c2, cp.int32(n)))   # grid, block, argumen
print(float(c[0]), float(c2[-1]))         # salin ke host hanya saat dicetak

# Periksa semua elemen di GPU, lalu ukur waktu kernel dengan CUDA event
assert bool(cp.all(c2 == 3.0)), "hasil RawKernel salah"
mulai, selesai = cp.cuda.Event(), cp.cuda.Event()
mulai.record()
for _ in range(10):
    tambah(((n + 255) // 256,), (256,), (a, b, c2, cp.int32(n)))
selesai.record()
selesai.synchronize()
ms = cp.cuda.get_elapsed_time(mulai, selesai) / 10
print(f"RawKernel: {ms:.3f} ms, bandwidth efektif {3 * a.nbytes / ms / 1e6:.1f} GB/s")

# Bandingkan biaya transfer: salin dari NumPy (host) ke GPU dan kembali
x = np.ones(n, dtype=np.float32)
for ulang in range(2):                    # putaran pertama = pemanasan (alokasi, inisialisasi)
    t0 = time.perf_counter()
    dx = cp.asarray(x)                    # host ke device
    hasil = cp.asnumpy(dx + dx)           # kernel + device ke host
    cp.cuda.Stream.null.synchronize()
    dt = (time.perf_counter() - t0) * 1e3
print(f"salin masuk + kernel + salin keluar: {dt:.1f} ms, hasil[0] = {hasil[0]}")
