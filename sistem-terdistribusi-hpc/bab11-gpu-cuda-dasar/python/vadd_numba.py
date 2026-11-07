"""Penjumlahan vektor dengan Numba CUDA (Kode 11.10).

Pemasangan: pip install numba-cuda[cu12]   (dukungan CUDA Numba kini di paket numba-cuda)
Jalankan: python vadd_numba.py
"""
import numpy as np
from numba import cuda


@cuda.jit
def tambah(a, b, c):
    i = cuda.grid(1)                       # = blockIdx.x * blockDim.x + threadIdx.x
    if i < c.size:
        c[i] = a[i] + b[i]


n = 1 << 24
da = cuda.to_device(np.ones(n, dtype=np.float32))       # salin ke GPU
db = cuda.to_device(np.full(n, 2.0, dtype=np.float32))
dc = cuda.device_array(n, dtype=np.float32)
tambah[(n + 255) // 256, 256](da, db, dc)               # [grid, block]
print(dc.copy_to_host()[:3])

# periksa semua elemen dan ukur waktu kernel (peluncuran pertama memuat JIT)
assert np.all(dc.copy_to_host() == 3.0), "hasil salah"
mulai, selesai = cuda.event(), cuda.event()
mulai.record()
for _ in range(10):
    tambah[(n + 255) // 256, 256](da, db, dc)
selesai.record()
selesai.synchronize()
ms = cuda.event_elapsed_time(mulai, selesai) / 10
print(f"kernel Numba: {ms:.3f} ms, bandwidth efektif {3 * 4 * n / ms / 1e6:.1f} GB/s")
