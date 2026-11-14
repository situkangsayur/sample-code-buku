# Bab 39: Algoritma di Sistem AI

| File | Isi | Kaitan di buku |
|---|---|---|
| `bpe.py` | pelatihan dan encoding BPE, contoh greedy yang tidak minimal, pembanding DP | Subbab 38.1 |
| `kv_cache.py` | attention satu head; hitung perkalian dengan dan tanpa KV cache; ukuran KV cache OPT-13B | Subbab 38.2 |
| `ann_graph.py` | graf k-NN dan greedy beam search (lapis bawah HNSW), recall vs ef | Subbab 38.3 |
| `rust/src/bin/*.rs` | `bpe`, `kv_cache`, `ann_graph` | versi Rust |

Menjalankan:

```
python3 bpe.py
cd rust && cargo test && cargo run --release --bin ann_graph
```

`ann_graph.py` membangun graf secara brute force, jadi butuh sekitar 10 detik di Python.
