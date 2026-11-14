# Bab 28 - Branch and Bound

Kode lengkap Bab 28 buku *Algoritma 101*. Instance knapsack bersama Bab 24, 25, 26, 27:
W = 10, barang (berat, nilai) 1=(5,10), 2=(4,40), 3=(6,30), 4=(3,50); optimum barang 2 dan 4, nilai 90.

| File | Isi | Kaitan di buku |
|---|---|---|
| `knapsack_bnb.py` | best-first branch and bound knapsack 0/1, batas fractional knapsack, uji silang brute force | Algoritma 28.1-25.2, Kode 28.1, Tabel 28.2, Gambar 28.1 |
| `assignment_bnb.py` | assignment problem 4x4 (matriks Levitin), batas minimum baris | Subbab 25.2, Gambar 28.2 |
| `tsp_bnb.py` | depth-first branch and bound TSP lima kota, batas sisi keluar termurah | Algoritma 28.3, Kode 28.3, Tabel 28.3 |
| `milp_knapsack.py` | knapsack sebagai MILP dengan `scipy.optimize.milp` (HiGHS) dan relaksasi LP | Kode 28.4 |
| `rust/src/bin/knapsack_bnb.rs` | padanan Rust knapsack_bnb (BinaryHeap), test uji silang | Kode 28.2 |
| `rust/src/bin/assignment_bnb.rs` | padanan Rust assignment | Subbab 25.2 |
| `rust/src/bin/tsp_bnb.rs` | padanan Rust TSP | Algoritma 28.3 |

Menjalankan:

```
python3 knapsack_bnb.py
python3 assignment_bnb.py
python3 tsp_bnb.py
python3 milp_knapsack.py      # butuh SciPy 1.9+; dilewati bila SciPy tidak ada
cd rust && cargo test && cargo run --bin knapsack_bnb && cargo run --bin assignment_bnb && cargo run --bin tsp_bnb
```
