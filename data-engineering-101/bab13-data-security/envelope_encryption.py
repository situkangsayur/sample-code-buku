"""Envelope encryption dengan AES-GCM. KMS disimulasikan oleh kunci lokal;
di produksi wrap/unwrap memanggil API KMS atau Vault Transit."""
import os

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

KEK = AESGCM(AESGCM.generate_key(bit_length=256))


def wrap(dek: bytes) -> bytes:
    n = os.urandom(12)
    return n + KEK.encrypt(n, dek, b"dek")


def unwrap(w: bytes) -> bytes:
    return KEK.decrypt(w[:12], w[12:], b"dek")


def enkripsi(data: bytes) -> tuple[bytes, bytes]:
    dek = AESGCM.generate_key(bit_length=256)
    n = os.urandom(12)
    c = n + AESGCM(dek).encrypt(n, data, None)
    return c, wrap(dek)


def dekripsi(c: bytes, w: bytes) -> bytes:
    return AESGCM(unwrap(w)).decrypt(c[:12], c[12:], None)


def rotasi(w: bytes, kek_baru: AESGCM) -> bytes:
    """Rotasi KEK: buka DEK dengan KEK lama, bungkus dengan KEK baru.
    Data (c) tidak disentuh sama sekali."""
    dek = unwrap(w)
    n = os.urandom(12)
    return n + kek_baru.encrypt(n, dek, b"dek")


if __name__ == "__main__":
    c, w = enkripsi(b"NIK=3201xxxxxxxx0001;saldo=12000000")
    print("plaintext :", dekripsi(c, w))
    print("ukuran DEK terbungkus:", len(w), "byte")
    kek2 = AESGCM(AESGCM.generate_key(bit_length=256))
    w2 = rotasi(w, kek2)
    dek = kek2.decrypt(w2[:12], w2[12:], b"dek")
    print("setelah rotasi:", AESGCM(dek).decrypt(c[:12], c[12:], None))
