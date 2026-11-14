# Bab 31. Kriptografi, Hash, dan Encryption

| File | Isi | Kaitan di buku |
|---|---|---|
| `rsa_mainan.py` | Square-and-multiply, extended Euclid, RSA mainan p = 61, q = 53 | Algoritma 31.1, Kode 31.2 |
| `hash_dua_jenis.py` | Hash polinomial untuk hash table vs SHA-256, efek avalanche | Kode 31.4 |
| `simpan_password.py` | Menyimpan password dengan salt dan scrypt (parameter OWASP) | Algoritma 31.2, Kode 31.1 dan 30.5 |
| `rust/src/bin/rsa_mainan.rs` | RSA mainan di Rust dengan u128 | Kode 31.3 |
| `rust/src/bin/hash_tabel.rs` | Hash polinomial dan tabrakan "Aa"/"BB" di Rust | Kode 31.4 |

RSA di sini HANYA untuk belajar. Untuk aplikasi nyata pakai library kriptografi yang
sudah diaudit. `simpan_password.py` butuh sekitar 128 MiB memori per panggilan scrypt.
Untuk Argon2id pakai paket `argon2-cffi` (Python) atau crate `argon2` (Rust).

Menjalankan:

```bash
python3 rsa_mainan.py && python3 hash_dua_jenis.py && python3 simpan_password.py
cd rust && cargo test && cargo run --bin rsa_mainan && cargo run --bin hash_tabel
```
