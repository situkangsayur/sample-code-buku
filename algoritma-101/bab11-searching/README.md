# Bab 11: Algoritma Mudah dan Searching

Kode lengkap Bab 11 buku *Algoritma 101*.

| File | Isi | Kaitan di buku |
|---|---|---|
| `algoritma_mudah.py`, `rust/src/bin/algoritma_mudah.rs` | maksimum dan posisinya, jumlah, tukar, cek prima, konversi biner | Algoritma 11.1–11.3, Kode 11.1–11.2, Tabel 11.3 |
| `linear_search.py`, `rust/src/bin/linear_search.rs` | linear search, hitung perbandingan, versi sentinel | Algoritma 11.4, Kode 11.3–11.4 |
| `binary_search.py`, `rust/src/bin/binary_search.rs` | binary search, jejak (lo, hi, mid), lower bound, uji acak terhadap `bisect` dan `slice::binary_search`, bug overflow `(lo + hi) / 2` | Algoritma 11.5, Kode 11.5–11.7, Tabel 11.1–11.2 |

Cara menjalankan:

```
python3 algoritma_mudah.py
python3 linear_search.py
python3 binary_search.py
cd rust
cargo test
cargo run --bin algoritma_mudah
cargo run --bin linear_search
cargo run --bin binary_search
```
