"""Hash untuk hash table dan cryptographic hash (Kode 32.4).

Fungsi hash_tabel meniru hash polinomial sederhana dari Bab 18.
SHA-256 dari hashlib adalah cryptographic hash.
Keduanya diuji dengan efek avalanche: ubah satu karakter, hitung bit yang berubah.
"""
import hashlib


def hash_tabel(s, m=2 ** 32):
    """Hash polinomial basis 31, cukup untuk hash table, tidak aman."""
    h = 0
    for ch in s:
        h = (h * 31 + ord(ch)) % m
    return h


def bit_berbeda(a, b):
    return bin(a ^ b).count("1")


def sha256_int(s):
    return int.from_bytes(hashlib.sha256(s.encode()).digest(), "big")


if __name__ == "__main__":
    a, b = "transfer 100", "transfer 101"
    print(hex(hash_tabel(a)), hex(hash_tabel(b)))
    print("hash_tabel bit berubah:", bit_berbeda(hash_tabel(a), hash_tabel(b)), "dari 32")
    print("sha256 bit berubah:", bit_berbeda(sha256_int(a), sha256_int(b)), "dari 256")
    print(hashlib.sha256(b"abc").hexdigest())
    assert hashlib.sha256(b"abc").hexdigest().startswith("ba7816bf")
    # tabrakan mudah pada hash polinomial: "Aa" dan "BB" sama-sama 2112
    assert hash_tabel("Aa") == hash_tabel("BB") == 2112
    assert bit_berbeda(hash_tabel(a), hash_tabel(b)) == 1
    assert 90 < bit_berbeda(sha256_int(a), sha256_int(b)) < 166
    print("semua uji lolos")
