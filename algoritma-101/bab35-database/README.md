# Bab 35: Algoritma di Dalam Database

Kode lengkap Bab 35 buku *Algoritma 101*.

| File | Isi | Kaitan di buku |
|---|---|---|
| `btree.py` | B-tree minimum degree t: insert dengan split, search dengan penghitung node, uji invarian | Algoritma 35.1, Kode 35.1, Gambar 35.1 |
| `lsm_bloom.py` | Bloom filter (double hashing), LSM-tree mini: memtable, SSTable, tombstone, compaction | Algoritma 35.2, Kode 35.3, Persamaan 34.2 |
| `join_dp.py` | urutan join dengan DP atas subset (gagasan System R) dibandingkan brute force | Algoritma 35.3, Kode 35.4, Tabel 35.2 |
| `explain_sqlite.py` | `EXPLAIN QUERY PLAN` SQLite sebelum dan sesudah index | Kode 35.5, Tabel 35.3 |
| `rust/src/bin/btree_search.rs` | B-tree di Rust dengan `binary_search` | Kode 35.2 |
| `rust/src/bin/bloom.rs` | Bloom filter di Rust, n = 1000, p = 0,01 | Subbab 34.4 |

Cara menjalankan (Python 3.12 dengan modul `sqlite3` bawaan; diuji dengan SQLite 3.45.1):

```
python3 btree.py
python3 lsm_bloom.py
python3 join_dp.py
python3 explain_sqlite.py
cd rust
cargo test
cargo run --bin btree_search
cargo run --bin bloom
```
