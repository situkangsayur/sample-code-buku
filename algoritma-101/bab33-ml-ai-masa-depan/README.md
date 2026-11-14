# Bab 33. Machine Learning, AI, dan Masa Depan Algoritma

| File | Isi | Kaitan di buku |
|---|---|---|
| `belajar_ambang.py` | ERM ambang satu dimensi dan batas sampel PAC | Algoritma 33.1, Kode 33.1 |
| `learned_index.py` | Learned index linear vs binary search pada 10^6 key | Algoritma 33.2 |
| `uji_stres.py` | Uji stres: solusi cepat yang salah vs brute force, lalu Kadane | Kode 33.2 |
| `rust/src/bin/belajar_ambang.rs` | ERM dan batas PAC di Rust | Algoritma 33.1 |
| `rust/src/bin/learned_index.rs` | Learned index di Rust | Algoritma 33.2 |
| `rust/src/bin/uji_stres.rs` | Uji stres di Rust | Kode 33.2 |

Menjalankan:

```bash
python3 belajar_ambang.py && python3 learned_index.py && python3 uji_stres.py
cd rust && cargo test && cargo run --bin uji_stres
```
