# Bab 19 - Tree dan Heap

| File | Isi | Kaitan di buku |
|---|---|---|
| `bst.py` | BST: sisip, cari, inorder, tinggi, hapus | Algoritma 19.1, Kode 19.1, Tabel 19.1 |
| `min_heap.py` | min-heap dari nol dan `heapq` | Algoritma 19.2-19.3, Kode 19.3-19.4, Tabel 19.3 |
| `rust/src/bin/bst.rs` | BST dengan `Option<Box<Node>>` | Kode 19.2 |
| `rust/src/bin/heap.rs` | min-heap dan `BinaryHeap` + `Reverse` | Kode 19.5 |

```bash
python3 bst.py && python3 min_heap.py
cd rust && cargo test && cargo run --bin bst && cargo run --bin heap
```
