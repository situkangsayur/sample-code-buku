# Bab 8 - Pengantar High Performance Computing

Contoh kode untuk Bab 8 buku *Sistem Terdistribusi dan Komputasi Berkinerja Tinggi*.

| Berkas | Kode di buku | Isi |
|---|---|---|
| `prima.go` | Kode 8.1 | Menghitung bilangan prima paralel dengan goroutine (pembagian cyclic, opsi `blok`) |
| `prima.py` | Kode 8.2 | Versi Python dengan `multiprocessing.Pool` |
| `jalankan.sh` | Kode 8.3 | Eksperimen strong scaling: pemanasan + 5 ulangan per p |
| `olah.py` | Kode 8.4 | Median, speedup, efisiensi, Karp-Flatt, kurva Amdahl |

## Menjalankan

```bash
# Go 1.22+ dan Python 3.10+
python3 -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt
./jalankan.sh                     # menghasilkan hasil.csv dan speedup.png

# versi Python
for p in 1 2 4; do python3 prima.py $p; done

# eksperimen pembagian blok (load imbalance)
go build -o prima prima.go && ./prima 4 20000000 blok
```

Catat lingkungan (`lscpu`, versi Go/Python) dan pastikan kolom jumlah prima sama untuk semua p.
