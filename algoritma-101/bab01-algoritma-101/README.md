# Bab 1 -- Algoritma 101

Contoh kode pendamping Bab 1 buku *Algoritma 101*.

| File | Isi | Kaitan di buku |
|---|---|---|
| `cari_nama.py` | linear search dan binary search pada 10.000 nama, menghitung perbandingan | Algoritma 1.1, 1.2; Kode 1.1 |
| `euclid.py` | algoritma Euclid versi pengurangan dan sisa bagi | Algoritma 1.3; Kode 1.2 |
| `rust/src/bin/cari_nama.rs` | versi Rust linear search dan binary search | Algoritma 1.1, 1.2 |
| `rust/src/bin/euclid.rs` | algoritma Euclid di Rust | Kode 1.3 |

Cara menjalankan:

```
python3 cari_nama.py
python3 euclid.py
cd rust && cargo test && cargo run --bin cari_nama && cargo run --bin euclid
```
