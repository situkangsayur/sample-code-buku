# Bab 28: Backtracking

Kode lengkap untuk Bab 28 buku *Algoritma 101*. Indeks di Python dan Rust mulai 0, sedangkan
*pseudocode* di buku mulai 1.

| File | Isi | Kaitan di buku |
|---|---|---|
| `nqueens.py` | n-Queens: semua solusi, versi himpunan kolom/diagonal, hitung node, tracing 4-Queens | Algoritma 28.2, Kode 28.1, Tabel 28.1 dan 24.2 |
| `sum_of_subsets.py` | Sum of subsets dengan dua syarat pemangkasan | Algoritma 28.3, Kode 28.3, Gambar 28.4 |
| `graph_coloring.py` | Pewarnaan graf m warna dan bilangan kromatik | Algoritma 28.4, Tabel 28.3, Gambar 28.5 |
| `sudoku.py` | Sudoku: backtracking polos dan pemilihan sel MRV | Algoritma 28.5, Kode 28.5, Tabel 28.4 |
| `regex_backtrack.py` | Waktu pencocokan pola `(a+)+$` di modul `re` | Kode 28.6 |
| `rust/src/bin/nqueens.rs` | n-Queens di Rust | Kode 28.2 |
| `rust/src/bin/sum_of_subsets.rs` | Sum of subsets di Rust | Algoritma 28.3 |
| `rust/src/bin/graph_coloring.rs` | Pewarnaan graf di Rust | Kode 28.4 |
| `rust/src/bin/sudoku.rs` | Sudoku dengan MRV di Rust | Algoritma 28.5 |

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
