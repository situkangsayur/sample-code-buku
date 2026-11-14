# Bab 32. Ketika Jawaban Eksak Terlalu Mahal

| File | Isi | Kaitan di buku |
|---|---|---|
| `enigma_ruang_kunci.py` | Ruang kunci Enigma tiga rotor dari lima, plugboard 10 kabel | Kode 32.1 |
| `las_vegas.py` | Algoritma Las Vegas: mencari 'a' secara acak | Subbab 31.3 |
| `miller_rabin.py` | Uji prima Miller-Rabin | Algoritma 32.1, Kode 32.2 |
| `vertex_cover.py` | 2-approximation vertex cover vs brute force | Algoritma 32.2 |
| `bloom.py` | Bloom filter dengan double hashing | Kode 32.3 |
| `hyperloglog.py` | HyperLogLog sederhana, p = 10 | Kode 32.4 |
| `rust/src/bin/*.rs` | Versi Rust: enigma_ruang_kunci, miller_rabin, bloom, vertex_cover | idem |

Menjalankan:

```bash
for f in *.py; do python3 "$f"; done
cd rust && cargo test && cargo run --bin bloom
```
