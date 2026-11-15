# Bab 24 - Algoritma Graf

Istilah, representasi, ADT, serta BFS/DFS dasar ada di `bab20-graf-struktur-data/`
(Bab 20, Jilid 1). `graf_representasi.py` di folder ini adalah salinan pendukung
yang diimpor `bfs_dfs.py`.

| File | Isi | Kaitan di buku |
|---|---|---|
| `graf_representasi.py` | adjacency list graf contoh (salinan dari Bab 20) | Gambar 24.1(a) |
| `bfs_dfs.py` | BFS dengan jarak dan parent, penyusunan path, DFS rekursif dan iteratif, komponen | Algoritma 24.1, Kode 24.1, Tabel 24.1, Gambar 24.2, subbab Komponen Terhubung |
| `topo_sort.py` | topological sort Kahn | Algoritma 24.2, Kode 24.3, Gambar 24.3 |
| `dfs_warna.py` | DFS tiga warna: deteksi cycle dan topological sort | Algoritma 24.3, Kode 24.4 |
| `rust/src/bin/bfs_dfs.rs` | BFS dan DFS di Rust | Kode 24.2 |
| `rust/src/bin/topo.rs` | Kahn di Rust | Algoritma 24.2 |
| `rust/src/bin/dfs_warna.rs` | DFS tiga warna di Rust | Algoritma 24.3 |

```bash
python3 graf_representasi.py && python3 bfs_dfs.py && python3 topo_sort.py && python3 dfs_warna.py
cd rust && cargo test && cargo run --bin bfs_dfs && cargo run --bin topo && cargo run --bin dfs_warna
```
