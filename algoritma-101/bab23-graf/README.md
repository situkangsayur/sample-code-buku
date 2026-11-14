# Bab 23 - Graf

| File | Isi | Kaitan di buku |
|---|---|---|
| `graf_representasi.py` | adjacency matrix dan adjacency list | Kode 23.1, Tabel 23.1, Gambar 23.1 |
| `bfs_dfs.py` | BFS, DFS rekursif dan iteratif, komponen | Algoritma 23.1-20.2, Kode 23.2, Tabel 23.3-20.4 |
| `topo_sort.py` | topological sort Kahn | Algoritma 23.3, Kode 23.4 |
| `rust/src/bin/bfs_dfs.rs` | BFS dan DFS di Rust | Kode 23.3 |
| `rust/src/bin/topo.rs` | Kahn di Rust | Algoritma 23.3 |

```bash
python3 graf_representasi.py && python3 bfs_dfs.py && python3 topo_sort.py
cd rust && cargo test && cargo run --bin bfs_dfs && cargo run --bin topo
```
