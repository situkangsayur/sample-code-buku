# Bab 21. Kembali ke Teori Bahasa dan Automata

| File | Isi | Kaitan di buku |
|---|---|---|
| `dfa_mod3.py` | DFA bilangan biner kelipatan 3 | Algoritma 21.1, Kode 21.1 |
| `anbn.py` | Pengenal a^n b^n dengan stack | Algoritma 21.2 |
| `collatz_anggaran.py` | Menjalankan program dengan anggaran langkah (semi-decidable) | Kode 21.3 |
| `rust/src/bin/dfa_mod3.rs` | DFA kelipatan 3 di Rust | Kode 21.2 |
| `rust/src/bin/anbn.rs` | a^n b^n di Rust | Algoritma 21.2 |
| `rust/src/bin/collatz_anggaran.rs` | Anggaran langkah di Rust | Kode 21.3 |

Menjalankan:

```bash
python3 dfa_mod3.py && python3 anbn.py && python3 collatz_anggaran.py
cd rust && cargo test && cargo run --bin dfa_mod3
```
