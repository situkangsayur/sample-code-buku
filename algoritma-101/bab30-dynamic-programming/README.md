# Bab 30. Dynamic Programming

Versi lengkap kode Bab 30 buku *Algoritma 101*. Instance knapsack 0/1 yang sama dipakai di Bab 25, 25, 26, dan 27:
W = 10, barang (berat, nilai) = (5, 10), (4, 40), (6, 30), (3, 50); optimal barang 2 dan 4, nilai 90.

| File | Isi | Kaitan di buku |
|---|---|---|
| `fibonacci.py` | Fibonacci memoization, tabulation, dan penghitung pemanggilan rekursi naif | Algoritma 30.1, 26.2, Kode 30.1, Gambar 30.1 |
| `koin_minimum.py` | Koin minimum dengan DP dan pembanding greedy | Algoritma 30.3, Kode 30.2, Tabel 30.2 |
| `knapsack_dp.py` | Tabel V[i][w], penelusuran balik, versi satu baris, uji silang brute force | Algoritma 30.4, 26.5, Kode 30.3, Gambar 30.2 |
| `lcs.py` | Tabel LCS dan penelusuran balik | Algoritma 30.6, Kode 30.5, Gambar 30.3 |
| `edit_distance.py` | Tabel edit distance Levenshtein | Algoritma 30.7, Gambar 30.4 |
| `floyd_warshall.py` | Floyd-Warshall dan pemeriksaan siklus negatif | Algoritma 30.8, Kode 30.7, Gambar 30.5, Tabel 30.3 |
| `rust/src/bin/fibonacci.rs` | Fibonacci memoization (HashMap) dan tabulation | Algoritma 30.1, 26.2 |
| `rust/src/bin/koin_minimum.rs` | Koin minimum, `usize::MAX` sebagai tak hingga | Algoritma 30.3 |
| `rust/src/bin/knapsack_dp.rs` | Tabel knapsack dan penelusuran balik | Kode 30.4 |
| `rust/src/bin/lcs.rs` | Panjang LCS | Algoritma 30.6 |
| `rust/src/bin/edit_distance.rs` | Edit distance | Kode 30.6 |
| `rust/src/bin/floyd_warshall.rs` | Floyd-Warshall dengan `Option<i64>` | Algoritma 30.8 |

## Menjalankan

```
python3 fibonacci.py
python3 koin_minimum.py
python3 knapsack_dp.py
python3 lcs.py
python3 edit_distance.py
python3 floyd_warshall.py

cd rust
cargo test
cargo run --bin knapsack_dp   # juga: fibonacci, koin_minimum, lcs, edit_distance, floyd_warshall
```

Setiap berkas Python menjalankan uji `assert` dan mencetak `semua uji lolos`.
