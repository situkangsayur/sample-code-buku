# Bab 6: Pseudocode

Kode pendamping Bab 6 buku *Algoritma 101*. Semua indeks di kode mulai dari 0, sedangkan
pseudocode di buku mulai dari 1; komentar di kode menyebut selisihnya.

| File | Isi | Kaitan di buku |
|---|---|---|
| `fungsi_prosedur.py` | Tukar, CariMaks, HitungMuncul, JumlahArray, RataRata, Balik | Algoritma 6.1--6.3, Kode 6.1, Latihan 6--8 |
| `rust/src/bin/fungsi_prosedur.rs` | Tukar (`&mut`), CariMaks, HitungMuncul, Balik | Kode 6.2, Latihan 10--11 |

Menjalankan:

```
python3 fungsi_prosedur.py
cd rust && cargo test && cargo run --bin fungsi_prosedur
```
