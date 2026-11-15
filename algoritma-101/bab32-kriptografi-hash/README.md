# Bab 32. Kriptografi, Hash, dan Encryption

| File | Isi | Kaitan di buku |
|---|---|---|
| `rsa_mainan.py` | Square-and-multiply, extended Euclid, RSA mainan p = 61, q = 53 | Algoritma 32.1, Kode 32.2 |
| `hash_dua_jenis.py` | Hash polinomial untuk hash table vs SHA-256, efek avalanche | Kode 32.4 |
| `simpan_password.py` | Menyimpan password dengan salt dan scrypt (parameter OWASP) | Algoritma 32.2, Kode 32.1 dan 30.5 |
| `rust/src/bin/rsa_mainan.rs` | RSA mainan di Rust dengan u128 | Kode 32.3 |
| `rust/src/bin/hash_tabel.rs` | Hash polinomial dan tabrakan "Aa"/"BB" di Rust | Kode 32.4 |

RSA di sini HANYA untuk belajar. Untuk aplikasi nyata pakai library kriptografi yang
sudah diaudit. `simpan_password.py` butuh sekitar 128 MiB memori per panggilan scrypt.
Untuk Argon2id pakai paket `argon2-cffi` (Python) atau crate `argon2` (Rust).

Menjalankan:

```bash
python3 rsa_mainan.py && python3 hash_dua_jenis.py && python3 simpan_password.py
cd rust && cargo test && cargo run --bin rsa_mainan && cargo run --bin hash_tabel
```
