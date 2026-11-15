# Bab 27. Divide and Conquer

Kode lengkap Bab 27 buku *Algoritma 101*. Indeks di Python dan Rust mulai dari 0, sedangkan
pseudocode di buku mulai dari 1.

| File | Isi | Kaitan di buku |
|---|---|---|
| `merge_sort.py` | merge sort, hitung perbandingan, uji stable | Algoritma MergeSort, Kode merge sort Python |
| `quick_sort.py` | partisi Lomuto, quick sort, pivot acak, worst case n(n-1)/2 | Algoritma QuickSort, Kode quick sort Python |
| `karatsuba.py` | perkalian Karatsuba untuk bilangan sepanjang apa pun | Algoritma Karatsuba, Kode Karatsuba Python |
| `closest_pair.py` | closest pair O(n log n) dengan daftar terurut x dan y | Algoritma ClosestPair |
| `fast_power.py` | pangkat cepat (biasa dan modulo), hitung perkalian | Algoritma FastPower, Coba Sendiri |
| `decrease_conquer.py` | binary search rekursif, insertion sort rekursif, Euclid | Algoritma InsertionSortRec, Kode binary search rekursif |
| `rust/src/bin/merge_sort.rs` | merge sort dengan slice | Kode merge sort Rust |
| `rust/src/bin/quick_sort.rs` | quick sort dengan `split_at_mut` | Kode quick sort Rust |
| `rust/src/bin/karatsuba.rs` | Karatsuba dengan `u128` | Algoritma Karatsuba |
| `rust/src/bin/closest_pair.rs` | closest pair (pita diurutkan ulang per panggilan) | Algoritma ClosestPair |
| `rust/src/bin/fast_power.rs` | pangkat cepat modulo m dengan `u128` | Kode pangkat cepat Rust |
| `rust/src/bin/decrease_conquer.rs` | binary search, insertion sort rekursif, Euclid | Subbab Decrease and Conquer |

## Menjalankan

```
python3 merge_sort.py        # dan berkas .py lainnya; setiap berkas menjalankan assert
cd rust
cargo test
cargo run --bin merge_sort   # quick_sort, karatsuba, closest_pair, fast_power, decrease_conquer
```
