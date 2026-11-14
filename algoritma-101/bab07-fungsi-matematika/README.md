# Bab 7: Fungsi Matematika sebagai Algoritma

Kode pendamping Bab 7 buku *Algoritma 101*.

| File | Isi | Kaitan di buku |
|---|---|---|
| `faktorial.py` | faktorial iteratif, Sigma dan Pi sebagai loop, rumus deret, prefix sum | Algoritma 7.1, Subbab 7.2--7.3 dan 7.5 |
| `euclid.py` | FPB Euclid, jejak tracing, KPK | Algoritma 7.2, Kode 7.2, Tabel 7.1 |
| `pangkat_cepat.py` | square-and-multiply, versi modulo, hitung banyak perkalian | Algoritma 7.3, Kode 7.4 |
| `newton_sqrt.py` | metode Newton untuk akar kuadrat dan isqrt bilangan bulat | Algoritma 7.4, Tabel 7.3 |
| `rust/src/bin/faktorial.rs` | faktorial dengan `checked_mul` | Kode 7.1 |
| `rust/src/bin/euclid.rs` | Euclid dengan `u64`; `%` dan `rem_euclid` | Kode 7.3 |
| `rust/src/bin/pangkat_cepat.rs` | pangkat cepat `u64` dan modulo dengan `u128` | Algoritma 7.3, Latihan 11 |
| `rust/src/bin/newton_sqrt.rs` | Newton `f64` dan isqrt, dicocokkan dengan `u64::isqrt` | Algoritma 7.4 |

Menjalankan:

```
python3 faktorial.py      # begitu pula berkas .py lain
cd rust && cargo test && cargo run --bin pangkat_cepat
```

`newton_sqrt.rs` memakai `u64::isqrt`, yang stabil sejak Rust 1.84 (Januari 2025).
