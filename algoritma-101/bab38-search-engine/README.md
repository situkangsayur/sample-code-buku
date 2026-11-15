# Bab 38: Algoritma di Search Engine

Kode lengkap Bab 38 buku *Algoritma 101*.

| File | Isi | Kaitan di buku |
|---|---|---|
| `inverted_index.py` | analyzer sederhana, inverted index dengan posisi, irisan posting list, phrase query | Algoritma 38.1, 36.2, Kode 38.1, Gambar 38.1 |
| `bm25.py` | TF-IDF dan BM25 (bentuk Lucene dan klasik, k1 = 1,2, b = 0,75) | Algoritma 38.3, Kode 38.3, Tabel 38.2 |
| `hnsw_mini.py` | HNSW mini: level acak, greedy per layer, beam search selebar ef; recall dibanding brute force | Algoritma 38.4, Kode 38.4, Tabel 38.3 |
| `rust/src/bin/irisan.rs` | irisan dua posting list terurut | Kode 38.2 |
| `rust/src/bin/bm25.rs` | inverted index + skor BM25 dengan `HashMap` | Subbab 36.3 |

Cara menjalankan (Python 3.12, Rust 1.81 atau lebih baru):

```
python3 inverted_index.py
python3 bm25.py
python3 hnsw_mini.py
cd rust
cargo test
cargo run --bin irisan
cargo run --bin bm25
```
