# Bab 27: Backtracking

Kode lengkap untuk Bab 27 buku *Algoritma 101*. Indeks di Python dan Rust mulai 0, sedangkan
*pseudocode* di buku mulai 1.

| File | Isi | Kaitan di buku |
|---|---|---|
| `nqueens.py` | n-Queens: semua solusi, versi himpunan kolom/diagonal, hitung node, tracing 4-Queens | Algoritma 27.2, Kode 27.1, Tabel 27.1 dan 24.2 |
| `sum_of_subsets.py` | Sum of subsets dengan dua syarat pemangkasan | Algoritma 27.3, Kode 27.3, Gambar 27.4 |
| `graph_coloring.py` | Pewarnaan graf m warna dan bilangan kromatik | Algoritma 27.4, Tabel 27.3, Gambar 27.5 |
| `sudoku.py` | Sudoku: backtracking polos dan pemilihan sel MRV | Algoritma 27.5, Kode 27.5, Tabel 27.4 |
| `regex_backtrack.py` | Waktu pencocokan pola `(a+)+$` di modul `re` | Kode 27.6 |
| `rust/src/bin/nqueens.rs` | n-Queens di Rust | Kode 27.2 |
| `rust/src/bin/sum_of_subsets.rs` | Sum of subsets di Rust | Algoritma 27.3 |
| `rust/src/bin/graph_coloring.rs` | Pewarnaan graf di Rust | Kode 27.4 |
| `rust/src/bin/sudoku.rs` | Sudoku dengan MRV di Rust | Algoritma 27.5 |

## Menjalankan

```
python3 nqueens.py
python3 sum_of_subsets.py
python3 graph_coloring.py
python3 sudoku.py
python3 regex_backtrack.py

cd rust
cargo test
cargo run --bin nqueens
cargo run --bin sum_of_subsets
cargo run --bin graph_coloring
cargo run --bin sudoku
```

Setiap program Python menjalankan uji `assert` dan mencetak `semua uji lolos`.
