# Bab 26 - Greedy

| File | Isi | Kaitan di buku |
|---|---|---|
| `greedy_dasar.py` | koin, activity selection, fractional knapsack, greedy knapsack 0/1 | Algoritma 26.2-22.3, Kode 26.1, Tabel 26.2 |
| `huffman.py` | Huffman coding dengan `heapq` | Algoritma 26.4, Kode 26.2, Tabel 26.3 |
| `graf_greedy.py` | Dijkstra, Prim, Kruskal (union-find), Dijkstra gagal pada bobot negatif | Algoritma 26.5-22.6, Kode 26.3 dan 22.5, Tabel 26.4-22.5 |
| `rust/src/bin/greedy_dasar.rs` | koin, activity selection, fractional knapsack | Algoritma 26.2-22.3 |
| `rust/src/bin/huffman.rs` | Huffman dengan `BinaryHeap` + `Reverse` | Algoritma 26.4 |
| `rust/src/bin/dijkstra.rs` | Dijkstra | Kode 26.4 |
| `rust/src/bin/kruskal.rs` | Kruskal dengan union-find | Algoritma 26.6 |

```bash
python3 greedy_dasar.py && python3 huffman.py && python3 graf_greedy.py
cd rust && cargo test && for b in greedy_dasar huffman dijkstra kruskal; do cargo run --bin $b; done
```
