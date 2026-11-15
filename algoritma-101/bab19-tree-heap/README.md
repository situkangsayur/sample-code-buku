# Bab 19 - Tree dan Heap

| File | Isi | Kaitan di buku |
|---|---|---|
| `nary_tree.py` | n-ary tree: list of children, preorder, postorder (ukuran folder), level-order, first-child next-sibling, indeks k-ary | Algoritma 19.1, Kode 19.1, Tabel 19.1, Gambar 19.2-19.3 |
| `bst.py` | BST: sisip, cari, inorder, tinggi, hapus | Algoritma 19.2, Kode 19.3, Tabel 19.2 |
| `min_heap.py` | min-heap dari nol dan `heapq` | Algoritma 19.3-19.4, Kode 19.5-19.6, Tabel 19.4 |
| `rust/src/bin/nary.rs` | n-ary tree dengan `Vec<Node>` | Kode 19.2 |
| `rust/src/bin/bst.rs` | BST dengan `Option<Box<Node>>` | Kode 19.4 |
| `rust/src/bin/heap.rs` | min-heap dan `BinaryHeap` + `Reverse` | Kode 19.7 |

```bash
python3 nary_tree.py && python3 bst.py && python3 min_heap.py
cd rust && cargo test && cargo run --bin nary && cargo run --bin bst && cargo run --bin heap
```
