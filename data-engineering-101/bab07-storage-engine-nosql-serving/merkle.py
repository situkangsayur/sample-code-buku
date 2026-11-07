"""Merkle tree: root hash, inclusion proof, dan verifikasinya (gaya RFC 6962:
daun di-hash dengan awalan 0x00, simpul dalam dengan awalan 0x01)."""
import hashlib


def H(b: bytes) -> bytes:
    return hashlib.sha256(b).digest()


def daun(data: bytes) -> bytes:
    return H(b"\x00" + data)


def simpul(kiri: bytes, kanan: bytes) -> bytes:
    return H(b"\x01" + kiri + kanan)


def root(level: list[bytes]) -> bytes:
    while len(level) > 1:
        if len(level) % 2:                 # jumlah ganjil: simpul terakhir naik apa adanya
            level = level + [None]
        level = [simpul(a, b) if b else a for a, b in zip(level[::2], level[1::2])]
    return level[0]


def bukti(level: list[bytes], i: int) -> list[tuple[str, bytes]]:
    """Inclusion proof untuk daun ke-i: daftar (sisi, hash saudara) dari bawah ke atas."""
    out = []
    while len(level) > 1:
        j = i ^ 1                          # indeks saudara
        if j < len(level):
            out.append(("kiri" if j < i else "kanan", level[j]))
        if len(level) % 2:
            level = level + [None]
        level = [simpul(a, b) if b else a for a, b in zip(level[::2], level[1::2])]
        i //= 2
    return out


def verifikasi(data: bytes, proof: list[tuple[str, bytes]], r: bytes) -> bool:
    x = daun(data)
    for sisi, s in proof:
        x = simpul(s, x) if sisi == "kiri" else simpul(x, s)
    return x == r


if __name__ == "__main__":
    trx = [f"trx {k}".encode() for k in range(1, 9)]          # 8 transaksi
    daun_ = [daun(t) for t in trx]
    r = root(daun_)
    p = bukti(daun_, 1)                                         # buktikan "trx 2"
    print("root:", r.hex()[:16], "...  panjang bukti:", len(p), "hash (log2 8 = 3)")
    print("trx 2 ada?", verifikasi(b"trx 2", p, r))
    print("trx 2 palsu?", verifikasi(b"trx 2 (diubah)", p, r))
