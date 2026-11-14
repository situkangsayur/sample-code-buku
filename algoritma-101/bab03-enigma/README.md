# Bab 3 -- Enigma dan Bletchley Park

| File | Isi | Kaitan di buku |
|---|---|---|
| `enigma.py` | simulator Enigma I (rotor I-V, reflector B, plugboard, double stepping); uji BDZGO | Subbab 3.1 (vektor uji BDZGO), Latihan 2 |
| `ruang_kunci.py` | menghitung ruang kunci Enigma I (lima rotor, sepuluh kabel) | Tabel 3.1, Subbab 3.2 |
| `crib.py` | menempatkan crib dengan sifat "tidak ada huruf yang menjadi dirinya sendiri" | Algoritma 3.1, contoh WETTERVORHERSAGE |
| `banburismus.py` | weight of evidence dalam deciban (peluang 1/17 dan 1/26 dari Alexander, sekitar 1945) | contoh Banburismus, Latihan 7 |
| `rust/src/bin/enigma.rs` | simulator Enigma di Rust, hasil sama dengan versi Python | bahan tambahan (tidak dirujuk langsung di buku) |
| `rust/src/bin/crib.rs` | penempatan crib di Rust | bahan tambahan (tidak dirujuk langsung di buku) |
| `rust/src/bin/ruang_kunci.rs` | ruang kunci dengan `u128` | bahan tambahan (tidak dirujuk langsung di buku) |

Cara menjalankan (jalankan `crib.py` dari folder ini karena mengimpor `enigma.py`):

```
python3 enigma.py && python3 ruang_kunci.py && python3 crib.py && python3 banburismus.py
cd rust && cargo test && cargo run --bin enigma && cargo run --bin crib && cargo run --bin ruang_kunci
```
