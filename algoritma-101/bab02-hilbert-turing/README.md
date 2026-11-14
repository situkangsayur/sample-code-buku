# Bab 2 -- Hilbert, Turing, dan Mesin di atas Kertas

| File | Isi | Kaitan di buku |
|---|---|---|
| `turing_machine.py` | simulator Turing machine satu pita, mesin penambah satu, mesin tanpa henti dengan batas langkah | Tabel 2.1, Subbab 2.3 |
| `automata.py` | finite automata kelipatan tiga dan pemeriksa kurung dengan stack | bahan tambahan untuk Gambar 2.2 (tidak dirujuk langsung di buku) |
| `rust/src/bin/turing_machine.rs` | simulator Turing machine di Rust | versi Rust dari simulator Python (tidak dirujuk langsung di buku) |
| `rust/src/bin/automata.rs` | DFA kelipatan tiga dan pemeriksa kurung di Rust | bahan tambahan (tidak dirujuk langsung di buku) |

Cara menjalankan:

```
python3 turing_machine.py
python3 automata.py
cd rust && cargo test && cargo run --bin turing_machine && cargo run --bin automata
```
