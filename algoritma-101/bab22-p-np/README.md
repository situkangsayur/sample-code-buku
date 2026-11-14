# Bab 22. P, NP, dan NP-Complete

| File | Isi | Kaitan di buku |
|---|---|---|
| `sat.py` | Verifier SAT dan brute force SAT (format literal ala DIMACS) | Algoritma 22.1, 29.2; Kode 22.1 |
| `vc_is.py` | Reduksi Independent Set ke Vertex Cover, diperiksa brute force | Contoh subbab 29.4 |
| `rust/src/bin/sat.rs` | Verifier dan brute force SAT di Rust | Kode 22.2 |
| `rust/src/bin/vc_is.rs` | Reduksi IS ke VC di Rust | Contoh subbab 29.4 |

Menjalankan:

```bash
python3 sat.py && python3 vc_is.py
cd rust && cargo test && cargo run --bin sat && cargo run --bin vc_is
```
