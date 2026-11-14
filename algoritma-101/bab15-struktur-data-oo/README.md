# Bab 15: Struktur Data dan Object Oriented

| File | Isi | Kaitan di buku |
|---|---|---|
| `point.py` | Class `Point`, pewarisan `Shape`/`Circle`/`Rectangle`, rujukan bersama | Kode 15.1, 15.2 |
| `dynamic_array.py` | Array dinamis: append, insert, remove_at, penghitung salinan | Algoritma 15.1, 15.2; Kode 15.5; Tabel 15.4 |
| `rust/src/bin/point.rs` | Struct, impl, trait `Shape`, `Box<dyn Shape>` | Kode 15.3, 15.4 |
| `rust/src/bin/dynamic_array.rs` | Array dinamis generik `DynArray<T>` | Kode 15.6 |

Menjalankan:

```
python3 point.py && python3 dynamic_array.py
cd rust && cargo test && cargo run --bin point && cargo run --bin dynamic_array
```
