# Bab 12 - Optimasi GPU dan Heterogeneous Computing

Contoh kode untuk Bab 12 buku *Sistem Terdistribusi dan Komputasi Berkinerja Tinggi*.
Semua program CUDA butuh GPU NVIDIA dan CUDA Toolkit (`nvcc`). Tanpa GPU lokal, pakai
Google Colab atau Kaggle dengan runtime GPU.

| Berkas | Isi | Kaitan di buku |
|---|---|---|
| `matmul.cu` | Perkalian matriks naif, tiled (shared memory), dan cuBLAS; pengukuran `cudaEvent`, GFLOPS, verifikasi | Kode 12.1, 12.2, 12.7, 12.8, 12.9 |
| `divergensi.cu` | Cabang divergen vs cabang per-warp | Kode 12.3 |
| `reduksi.cu` | Reduction pohon di shared memory + `atomicAdd` | Kode 12.4 |
| `scan.cu` | Exclusive scan Blelloch satu block | Algoritma 12.2 |
| `histogram.cu` | Histogram naif vs privatization | Kode 12.5 |
| `stream.cu` | Tumpang tindih transfer dan kernel dengan CUDA stream | Kode 12.6 |
| `roofline.py` | Menggambar roofline dan titik hasil ukur | Gambar 12.7 |

## Menjalankan

```bash
make ARCH=sm_75            # T4 di Colab; ganti sesuai GPU (lihat nvidia-smi)
./matmul 2048              # keluaran CSV: versi,N,TILE,ms,GFLOPS,galat_relatif
make matmul32 && ./matmul32 2048
make info                  # register dan shared memory per kernel
./histogram && ./reduksi && ./scan && ./stream 4 && ./divergensi
pip install -r requirements.txt
python roofline.py contoh_hasil.csv --puncak 8100 --bw 320
```

Di Colab, tulis berkas dengan sel `%%writefile matmul.cu`, lalu jalankan `!make` dan `!./matmul 2048`.

Profiling:

```bash
nsys profile -o lini ./stream 4        # lini waktu: transfer, kernel, stream
ncu --set full -k matmulTiled ./matmul 1024   # metrik per kernel: occupancy, throughput memori
```
