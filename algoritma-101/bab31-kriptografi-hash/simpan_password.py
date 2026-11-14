"""Menyimpan dan memeriksa password dengan salt dan scrypt (Algoritma 31.2, Kode 31.5).

Rekomendasi OWASP (diakses 14 November 2026): Argon2id lebih dulu
(m = 19 MiB, t = 2, p = 1); bila tidak tersedia, scrypt dengan
N = 2^17, r = 8, p = 1. Pustaka standar Python tidak punya Argon2id,
jadi contoh ini memakai hashlib.scrypt. Untuk Argon2id di Python
pakai paket argon2-cffi; di Rust pakai crate argon2.
"""
import hashlib
import hmac
import os
import time

N, R, P = 2 ** 17, 8, 1          # parameter minimum OWASP untuk scrypt
MAXMEM = 256 * 1024 * 1024       # 128 MiB dibutuhkan; beri ruang lebih


def buat_hash(password):
    salt = os.urandom(16)        # salt acak, unik per pengguna
    dk = hashlib.scrypt(password.encode(), salt=salt, n=N, r=R, p=P,
                        maxmem=MAXMEM, dklen=32)
    return f"scrypt${N}${R}${P}${salt.hex()}${dk.hex()}"


def periksa(password, tersimpan):
    _, n, r, p, salt_hex, dk_hex = tersimpan.split("$")
    dk = hashlib.scrypt(password.encode(), salt=bytes.fromhex(salt_hex),
                        n=int(n), r=int(r), p=int(p), maxmem=MAXMEM, dklen=32)
    return hmac.compare_digest(dk, bytes.fromhex(dk_hex))   # waktu konstan


def laju_sha256(detik=0.5):
    """Berapa SHA-256 per detik di mesin ini (untuk perbandingan)."""
    n, mulai = 0, time.perf_counter()
    while time.perf_counter() - mulai < detik:
        hashlib.sha256(b"password123").digest()
        n += 1
    return n / detik


if __name__ == "__main__":
    t0 = time.perf_counter()
    h1 = buat_hash("rahasia-Tazkia-2026")
    lama = time.perf_counter() - t0
    h2 = buat_hash("rahasia-Tazkia-2026")
    print(h1[:60] + "...")
    print("salt berbeda, hash berbeda:", h1 != h2)
    print(f"satu scrypt: {lama:.3f} detik")
    print(f"SHA-256 polos: {laju_sha256():,.0f} per detik")
    assert periksa("rahasia-Tazkia-2026", h1)
    assert not periksa("rahasia-tazkia-2026", h1)
    assert h1 != h2
    print("semua uji lolos")
