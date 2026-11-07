"""Crypto-shredding: menghapus data dengan menghancurkan kunci per nasabah."""
import os

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

kunci = {}


def tulis(nasabah: str, pii: str) -> bytes:
    k = kunci.setdefault(nasabah, AESGCM.generate_key(bit_length=256))
    n = os.urandom(12)
    return n + AESGCM(k).encrypt(n, pii.encode(), nasabah.encode())


def baca(nasabah: str, blob: bytes) -> str:
    k = kunci.get(nasabah)
    if k is None:
        return "<dihapus>"
    return AESGCM(k).decrypt(blob[:12], blob[12:], nasabah.encode()).decode()


if __name__ == "__main__":
    arsip = tulis("N42", "Siti; 3201011234560001; 081234567890")
    backup = bytes(arsip)                 # salinan di tier dingin
    print(baca("N42", arsip))
    del kunci["N42"]                      # permintaan hapus dipenuhi
    print(baca("N42", arsip), baca("N42", backup))
