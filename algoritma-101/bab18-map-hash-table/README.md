# Bab 18 - Map dan Hash Table

Kode pendamping Bab 18 buku *Algoritma 101*.

| File | Isi | Kaitan di buku |
|---|---|---|
| `hash_chaining.py` | hash table separate chaining, rehashing | Algoritma 18.2, Kode 18.1, Gambar 18.2 |
| `hash_linear_probing.py` | linear probing, tombstone, rehashing | Algoritma 18.3, Tabel 18.2, Gambar 18.3 |
| `dict_python.py` | polynomial hash, hitung kata, sifat `dict` | Algoritma 18.1, Kode 18.4 |
| `ukur_list_dict.py` | ukur `x in list` vs `x in dict` | pembuka bab |
| `rust/src/bin/chaining.rs` | separate chaining di Rust | Kode 18.2 |
| `rust/src/bin/linear_probing.rs` | linear probing dengan `enum Slot` | Kode 18.3 |
| `rust/src/bin/hashmap_demo.rs` | `HashMap` dan entry API | Kode 18.5 |

Cara menjalankan:

```bash
python3 hash_chaining.py && python3 hash_linear_probing.py && python3 dict_python.py
python3 ukur_list_dict.py      # hasil waktu bergantung mesin
cd rust && cargo test && cargo run --bin chaining && cargo run --bin linear_probing && cargo run --bin hashmap_demo
```
