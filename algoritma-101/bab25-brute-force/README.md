# Bab 25 - Brute Force dan Exhaustive Search

Instance kecil di sini dipakai lagi di Bab 26, 25, 26, dan 27:
TSP empat kota (optimal A-B-D-C-A = 18), knapsack 0/1 W = 10 dengan
(berat, nilai) = (5,10), (4,40), (6,30), (3,50) (optimal barang 2 dan 4 = 90;
varian barang 3 = (7,63) optimal 113), dan assignment 4x4 (optimal 13).

| File | Isi | Kaitan di buku |
|---|---|---|
| `string_matching.py` | string matching naif + hitung perbandingan | Algoritma 25.1, Kode 25.1, Tabel 25.2 |
| `closest_pair.py` | closest pair naif | Algoritma 25.2, Kode 25.2 |
| `exhaustive.py` | TSP, knapsack 0/1, assignment | Algoritma 25.3-21.4, Kode 25.3, Tabel 25.3 dan 21.5 |
| `rust/src/bin/string_matching.rs` | versi Rust string matching | Algoritma 25.1 |
| `rust/src/bin/closest_pair.rs` | versi Rust closest pair | Algoritma 25.2 |
| `rust/src/bin/exhaustive.rs` | permutasi, TSP, knapsack bit mask, assignment | Kode 25.4 |

```bash
python3 string_matching.py && python3 closest_pair.py && python3 exhaustive.py
cd rust && cargo test && cargo run --bin string_matching && cargo run --bin closest_pair && cargo run --bin exhaustive
```
