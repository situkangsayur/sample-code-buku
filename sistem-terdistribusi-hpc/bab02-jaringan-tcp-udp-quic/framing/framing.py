"""Kode 2.6: framing awalan panjang 4 byte (Algoritma 2.1)."""
import struct

MAKS = 16 * 1024 * 1024  # tolak pesan > 16 MB


def kirim_pesan(sock, data: bytes):
    sock.sendall(struct.pack("!I", len(data)) + data)  # !I = uint32 big-endian


def baca_tepat(sock, n: int) -> bytes:
    buf = bytearray()
    while len(buf) < n:
        potong = sock.recv(n - len(buf))  # bisa kurang dari yang diminta
        if not potong:
            raise ConnectionError("koneksi ditutup di tengah pesan")
        buf += potong
    return bytes(buf)


def terima_pesan(sock) -> bytes:
    (panjang,) = struct.unpack("!I", baca_tepat(sock, 4))
    if panjang > MAKS:
        raise ValueError(f"pesan terlalu besar: {panjang}")
    return baca_tepat(sock, panjang)
