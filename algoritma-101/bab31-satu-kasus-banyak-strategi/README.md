# Bab 31 - Satu Kasus, Banyak Strategi

Kode lengkap Bab 31 buku *Algoritma 101*: satu instance knapsack 0/1 (W = 10; barang
(5,10), (4,40), (6,30), (3,50)) diselesaikan dengan brute force, greedy, branch and bound, dan DP.

| File | Isi | Kaitan di buku |
|---|---|---|
| `knapsack_strategi.py` | enam fungsi (brute force, greedy nilai/berat/rasio, B&B best-first dan depth-first, DP), varian (7,63) yang menggagalkan greedy rasio, instance acak n = 10..40, uji skala berat x1000, instance rasio sama | Kode 31.1, 27.2, 27.4; Algoritma 31.1-27.2; Tabel 31.1-27.5; Gambar 31.1-27.2 |
| `rust/src/bin/knapsack_strategi.rs` | brute force, greedy rasio (perkalian silang), B&B depth-first, DP; test uji silang 300 instance | Kode 31.3, Algoritma 31.2 |

Menjalankan (Python sekitar 6 detik karena instance rasio sama n = 20):

```
python3 knapsack_strategi.py
cd rust && cargo test && cargo run --bin knapsack_strategi
```
