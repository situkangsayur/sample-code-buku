# Bab 20 - Graf sebagai Struktur Data

| File | Isi | Kaitan di buku |
|---|---|---|
| `graf_representasi.py` | edge list, adjacency matrix, adjacency list | Kode 20.1, Tabel 20.1-20.2, Gambar 20.2 dan 20.4 |
| `graf_adt.py` | ADT graf (dict of set): tambah/hapus vertex dan edge, cek edge, tetangga, in/out-degree | Kode 20.2, contoh operasi ADT, Gambar 20.3(a) |
| `telusur.py` | BFS, DFS rekursif, DFS iteratif, urutan selesai | Algoritma 20.1-20.2, Kode 20.4, Tabel 20.3-20.4 |
| `rust/src/bin/graf_adt.rs` | ADT graf dengan `Vec<Vec<usize>>` | Kode 20.3 |
| `rust/src/bin/telusur.rs` | BFS dan DFS iteratif | Kode 20.5 |

Jarak dan parent BFS, komponen terhubung, topological sort, dan deteksi cycle
ada di folder `bab24-graf/` (Bab 24, Jilid 2).

```bash
python3 graf_representasi.py && python3 graf_adt.py && python3 telusur.py
cd rust && cargo test && cargo run --bin graf_adt && cargo run --bin telusur
```
