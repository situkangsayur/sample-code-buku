# Bab 12: Sorting Sederhana dan Kebenaran Algoritma

Kode lengkap Bab 12 buku *Algoritma 101*.

| File | Isi | Kaitan di buku |
|---|---|---|
| `sorting.py` | bubble, selection, insertion sort; menghitung perbandingan dan tukar/geser | Algoritma 12.1–12.3, Kode 12.1–12.2, Tabel 12.1–12.4 |
| `uji_sorting.py` | kasus batas, uji acak terhadap `sorted`, assert loop invariant, uji stabilitas | Kode 12.5–12.6, Tabel 12.6, Subbab 12.5 |
| `rust/src/bin/sorting.rs` | ketiga sort di Rust dengan `#[test]` kasus batas dan uji acak | Kode 12.4 |
| `contoh-error/insertion_usize.rs` | insertion sort dengan `j: usize` yang underflow, beserta keluaran `rustc` 1.94 | Kode 12.3 |

Cara menjalankan:

```
python3 sorting.py
python3 uji_sorting.py
cd rust
cargo test
cargo run --bin sorting
```
