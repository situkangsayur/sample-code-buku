# Bab 35: Algoritma di Dalam Bahasa Pemrograman

Kode lengkap Bab 35 buku *Algoritma 101*.

| File | Isi | Kaitan di buku |
|---|---|---|
| `timsort_mini.py` | Timsort sederhana (run alami, minrun, binary insertion, merge) dengan merge policy Powersort | Algoritma 35.1, Kode 35.1, Tabel 35.2 |
| `dict_probe.py` | urutan probing `dict` CPython dan model compact dict (indices + entries) | Algoritma 35.2, Kode 35.3, Gambar 35.2 |
| `pertumbuhan_list.py` | kapasitas `list` CPython lewat `sys.getsizeof`, model biaya salin tiga aturan pertumbuhan | Kode 35.4, Tabel 35.4, Gambar 35.3 |
| `rust/src/bin/natural_merge.rs` | natural merge sort stabil (gagasan bersama Timsort dan driftsort) | Subbab 33.1.3 |
| `rust/src/bin/sort_stabil.rs` | `sort_by_key` (driftsort), `sort_unstable_by_key` (ipnsort), `total_cmp` untuk `f64` | Kode 35.2 |
| `rust/src/bin/vec_growth.rs` | kapasitas `Vec<u64>` saat `push` dan efek `with_capacity` | Kode 35.5, Gambar 35.3 |

Cara menjalankan (Python 3.12, Rust 1.81 atau lebih baru; angka kapasitas diuji dengan CPython 3.12.3 dan Rust 1.94):

```
python3 timsort_mini.py
python3 dict_probe.py
python3 pertumbuhan_list.py
cd rust
cargo test
cargo run --bin natural_merge
cargo run --bin sort_stabil
cargo run --bin vec_growth
```

Deret kapasitas `list` dan `Vec` adalah detail implementasi dan dapat berubah di versi lain.
