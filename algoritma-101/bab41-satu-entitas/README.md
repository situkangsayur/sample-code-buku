# Bab 41: Satu Entitas di Program, Database, dan API

| File | Isi | Kaitan di buku |
|---|---|---|
| `mahasiswa.py` | dataclass Mahasiswa, JSON dan validasi schema sederhana, tabel SQLite dengan index komposit, EXPLAIN QUERY PLAN, pagination offset dan cursor, dokumen | Subbab 39.1-39.3 |
| `rust/src/bin/mahasiswa.rs` | struct Mahasiswa, JSON manual, index komposit dengan BTreeMap, pagination offset dan cursor | versi Rust |

Hanya library standar (Python: dataclasses, json, sqlite3; Rust: std).

```
python3 mahasiswa.py
cd rust && cargo test && cargo run --bin mahasiswa
```
