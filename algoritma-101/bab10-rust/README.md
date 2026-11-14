# Bab 10: Dari Pseudocode ke Rust

Kode lengkap Bab 10 buku *Algoritma 101*.

| File | Isi | Kaitan di buku |
|---|---|---|
| `rust/src/bin/padanan.rs` | maksimum, jumlah deret, FPB, faktorial `u128`, `loop` + `break`, `match` | Kode 10.3–10.4, Tabel 10.1 |
| `rust/src/bin/vec_range.rs` | range `a..b` dan `a..=b`, `Vec`, slice, `get` | Kode 10.5 |
| `rust/src/bin/overflow.rs` | batas tipe bulat, `checked_*`, `wrapping_*`, `saturating_*`, panic di profil dev | Kode 10.6–10.7, Tabel 10.2 |
| `rust/src/bin/ownership.rs` | move, `&`, `&mut`, `clone`, tipe `Copy` | Kode 10.8 |
| `contoh-error/*.rs` | program yang sengaja salah, beserta keluaran `rustc` 1.94 di `*.keluaran.txt` | Kode 10.1, 10.9–10.10, Tabel 10.3, Subbab 10.6 |

Cara menjalankan (Rust 1.81 atau lebih baru):

```
cd rust
cargo test
cargo run --bin padanan
cargo run --bin vec_range
cargo run --bin ownership
cargo run --bin overflow                      # keluar normal
cargo run --bin overflow -- panik             # profil dev: panic "attempt to add with overflow"
cargo run --release --bin overflow -- panik   # profil release: hasil wrapping (4)
```

Contoh error tidak termasuk crate. Untuk melihat pesannya sendiri:

```
cd contoh-error
rustc --edition 2021 e0384_immutable.rs
```
