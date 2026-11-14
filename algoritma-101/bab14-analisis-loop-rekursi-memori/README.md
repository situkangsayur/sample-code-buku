# Bab 14: Menganalisis Loop, Rekursi, dan Memori

| File | Isi | Kaitan di buku |
|---|---|---|
| `loops.py` | Banyak iterasi pola loop dicocokkan dengan rumus | Tabel 14.1; Kode 14.1 |
| `recurrences.py` | Faktorial, binary search rekursif, T(n)=2T(n/2)+n, pemanggilan Fibonacci | Subbab 14.2; Algoritma 14.2 |
| `space.py` | Membalik di tempat vs salinan, rekursi dan RecursionError | Algoritma 14.3; Kode 14.2 |
| `amortized.py` | Simulasi array dinamis berlipat dua dan titik tumbuh `list` CPython | Tabel 14.4; Kode 14.3 |
| `benchmark.py` | Pengukuran O(n) dan O(n^2) di Python | Kode 14.4; Tabel 14.6 |
| `rust/src/bin/benchmark.rs` | Pengukuran yang sama di Rust dengan `black_box` | Kode 14.5; Tabel 14.6 |
| `rust/src/bin/vec_capacity.rs` | Kapan kapasitas `Vec` berubah | Subbab 14.4 |
| `rust/src/bin/loops.rs` | Loop segitiga dan pembagian dua | Tabel 14.1 |

Menjalankan:

```
for f in loops recurrences space amortized benchmark; do python3 $f.py; done
cd rust && cargo test
cargo run --release --bin benchmark   # selalu --release untuk pengukuran
cargo run --bin vec_capacity && cargo run --bin loops
```

Angka waktu bergantung mesin. Angka di buku: Intel Xeon E5-2697 v4, Python 3.12.3, Rust 1.94.0, 14 November 2026.
