# Bab 9 - CPU, Memori, dan OpenMP

Contoh kode untuk Bab 9 buku *Sistem Terdistribusi dan Komputasi Berkinerja Tinggi*.
Butuh Linux/WSL dengan `gcc` (dukungan OpenMP), `g++`, Python 3.10+, dan Rust (rustup) untuk contoh Rust.

| Folder/berkas | Kode di buku | Isi |
|---|---|---|
| `memori/bug.c` | Kode 9.1-9.2 | Empat bug memori klasik (sengaja salah), dijalankan dengan AddressSanitizer |
| `memori/raii.cpp` | Kode 9.3 | RAII, `unique_ptr`, `shared_ptr` |
| `memori/refcount.py` | Kode 9.4 | Reference counting dan cycle collector CPython |
| `rust-ownership/` | Kode 9.5 | Ownership, borrowing, `Arc` |
| `core/ilp.c` | Kode 9.6 | Satu vs empat akumulator (ILP) |
| `core/branch.c` | Kode 9.7 | Branch prediction: data acak vs terurut, versi tanpa cabang |
| `core/rowcol.c` | Kode 9.8 | Penjumlahan per baris vs per kolom |
| `core/false_sharing.c` | Kode 9.9 | False sharing dan padding 64 byte |
| `openmp/first_touch.c` | Kode 9.10 | Inisialisasi serial vs paralel (NUMA first touch) |
| `simd/saxpy.c` | Kode 9.11-9.12 | saxpy dan laporan auto-vectorization (`make laporan`) |
| `simd/aos_soa.c` | Kode 9.13 | Array of Structures vs Structure of Arrays |
| `simd/dot_avx.c` | Kode 9.14 | Dot product dengan intrinsics AVX2 + FMA |
| `openmp/halo.c` | Kode 9.15-9.16 | Program OpenMP pertama |
| `openmp/pi_salah.c`, `openmp/pi_omp.c` | Kode 9.17-9.18 | Race condition vs `reduction` |
| `openmp/prima_omp.c` | Kode 9.19 | `schedule(runtime)`: coba `OMP_SCHEDULE=static` vs `dynamic,1000` |
| `rust-rayon/` | Kode 9.20 | Pi dengan Rayon |
| `python/pi_numba.py` | Kode 9.21 | Pi dengan Numba `prange` |
| `matmul/` | Kode 9.22-9.25 | Perkalian matriks versi 1-5 + pembanding NumPy/BLAS |

Nomor Kode mengikuti urutan di buku dan dapat bergeser sedikit bila buku direvisi.

## Menjalankan

```bash
make -C memori && ./memori/bug; ./memori/raii; python3 memori/refcount.py
(cd rust-ownership && cargo run)
make -C core && ./core/ilp && ./core/branch && ./core/rowcol 4096
./core/false_sharing 0; ./core/false_sharing 1
make -C simd laporan && make -C simd && ./simd/saxpy && ./simd/aos_soa && ./simd/dot_avx
make -C openmp && OMP_NUM_THREADS=4 ./openmp/halo
for p in 1 2 4 8; do OMP_NUM_THREADS=$p ./openmp/pi_omp; done
OMP_SCHEDULE=static ./openmp/prima_omp; OMP_SCHEDULE=dynamic,1000 ./openmp/prima_omp
(cd rust-rayon && RAYON_NUM_THREADS=4 cargo run --release)
pip install -r python/requirements.txt && python3 python/pi_numba.py

# Praktikum perkalian matriks
make -C matmul cek          # uji kebenaran pada n = 256
make -C matmul bench N=2048 # versi 1-5
python3 matmul/bench_numpy.py 2048
make -C matmul perf         # cache miss versi 1 vs 2 (butuh perf)
```
