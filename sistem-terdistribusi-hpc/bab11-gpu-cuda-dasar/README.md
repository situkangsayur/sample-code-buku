# Bab 11 - GPU dan CUDA Dasar

Contoh kode untuk Bab 11 buku *Sistem Terdistribusi dan Komputasi Berkinerja Tinggi*.
Semua program CUDA butuh GPU NVIDIA dan CUDA Toolkit (`nvcc`). Tanpa GPU lokal, pakai
Google Colab atau Kaggle dengan runtime GPU (lihat `colab.ipynb`). Setiap berkas `.cu`
berdiri sendiri (makro `CEK` ditulis di tiap berkas) agar mudah disalin ke sel Colab.

| Berkas | Isi | Kaitan di buku |
|---|---|---|
| `vadd.cu` | Kernel `tambah`, makro `CEK`, lima langkah program CUDA, pemeriksaan semua elemen | Kode 11.2, 11.6, 11.7, 11.8 |
| `stencil1d.cu` | Stencil 1D (R = 3) dengan shared memory dan `__syncthreads`, dibandingkan versi memori global dan CPU | Kode 11.5 |
| `matmul.cu` | Perkalian matriks naif (satu thread per elemen C), ukuran block sebagai argumen, GFLOPS, verifikasi CPU | Kode 11.3, 11.11 |
| `vadd_ukur.cu` | Waktu CPU, salin masuk, kernel (`cudaEvent`, median), salin keluar, bandwidth efektif, speedup kernel dan total; opsi pinned memory | Kode 11.12, Tabel 11.7 |
| `python/vadd_cupy.py` | Penjumlahan vektor dengan CuPy: operasi array dan `RawKernel` | Kode 11.9 |
| `python/vadd_numba.py` | Penjumlahan vektor dengan Numba CUDA (`numba-cuda`) | Kode 11.10 |
| `colab.ipynb` | Notebook praktikum: cek GPU, tulis berkas dengan `%%writefile`, kompilasi, ukur | Kode 11.13, Subbab 11.9 |

## Menjalankan

```bash
nvidia-smi --query-gpu=name,compute_cap --format=csv   # mis. 7.5 -> sm_75
make ARCH=sm_75            # T4 di Colab; RTX 30xx: ARCH=sm_86
./vadd                     # c[0] = 3.0, c[n-1] = 3.0
./stencil1d
./matmul 1024              # block 16x16
./matmul 1024 32           # block 32x32
./matmul 512 64            # block 64x64: gagal diluncurkan dan terdeteksi cudaGetLastError
./vadd_ukur 24             # baris CSV untuk tabel praktikum
./vadd_ukur 26 pinned      # salinan dengan pinned memory (cudaMallocHost)
make ukur                  # seluruh isian tabel praktikum sekaligus

python -m venv .venv && source .venv/bin/activate
pip install -r python/requirements.txt
python python/vadd_cupy.py
python python/vadd_numba.py
```

Di Colab, unggah `colab.ipynb` (File -> Upload notebook), pilih runtime T4 GPU, lalu jalankan
semua sel.

## Catatan hasil ukur

- `vadd_ukur` mencetak dua speedup: terhadap waktu kernel saja dan terhadap waktu total
  (salin masuk + kernel + salin keluar). Untuk penjumlahan vektor, speedup total biasanya di
  bawah 1 dengan memori biasa (pageable) karena transfer PCIe mendominasi.
- Pada GPU modern, `stencil1d` versi memori global bisa hampir secepat versi shared memory
  karena cache L1/L2 ikut menyerap pembacaan ulang. Selisihnya lebih jelas pada radius besar.
- Perkalian matriks naif sering jauh melampaui batas 0,25 FLOP/byte dari analisis kasar,
  karena thread dalam satu warp berbagi baris A dan cache L1/L2 memakai ulang data. Versi
  tiled di Bab 12 tetap lebih cepat dan lebih dapat diandalkan.

Profiling (Nsight, bukan `nvprof` yang sudah usang):

```bash
nsys profile -o lini ./vadd_ukur 24
ncu -k matmul ./matmul 1024
```
