# Bab 21: Analisis Algoritma secara Lebih Teliti

| File | Isi | Kaitan di buku |
|---|---|---|
| `sums.py` | Loop pembagi (harmonik), loop sampai i^2, loop pelipatan dua, batas log2 n! | Algoritma 21.1; Kode 21.1; Tabel 21.2-20.3 |
| `recurrences.py` | T(n) tepat untuk substitusi, recursion tree tak seimbang, tiga kasus teorema master | Subbab 20.3 |
| `average_case.py` | Rata-rata tepat atas semua permutasi: geseran insertion sort, penggantian maksimum | Algoritma 21.2; Kode 21.3; Tabel 21.4 |
| `amortized.py` | Counter biner (agregat, potential) dan array dinamis dengan Phi = 2 size - cap | Algoritma 21.3; Gambar 21.3; Tabel 21.5 |
| `sort_lower_bound.py` | ceil(log2 n!) vs worst case merge/insertion sort; hitung perbandingan `sorted()` | Tabel 21.6; Kode 21.5 |
| `rust/src/bin/sums.rs` | Loop pembagi dan pelipatan dua | Kode 21.2 |
| `rust/src/bin/counter.rs` | Counter biner dan pemeriksaan potential | Kode 21.4 |
| `rust/src/bin/sort_lower_bound.rs` | Worst case merge sort atas semua permutasi; hitung perbandingan `sort_by` | Kode 21.6 |

Menjalankan:

```
for f in sums recurrences average_case amortized sort_lower_bound; do python3 $f.py; done
cd rust && cargo test
cargo run --release --bin sums && cargo run --release --bin counter && cargo run --release --bin sort_lower_bound
```

Banyak perbandingan `sorted()` dan `sort_by` bergantung pada versi bahasa dan data. Angka di buku:
Intel Xeon E5-2697 v4, Python 3.12.3, Rust 1.94.0, 15 November 2026.
