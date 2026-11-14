"""Bab 36: Merkle tree, akar, dan bukti keanggotaan (Merkle proof).

Leaf = H(data). Node dalam = H(kiri || kanan). Bila banyak node di
satu level ganjil, node terakhir dipasangkan dengan dirinya sendiri.
Bukti untuk satu leaf berisi hash saudara di setiap level: O(log n).
"""
import hashlib


def H(b):
    return hashlib.sha256(b).digest()


def level_atas(level):
    if len(level) % 2 == 1:
        level = level + [level[-1]]
    return [H(level[i] + level[i + 1]) for i in range(0, len(level), 2)]


def merkle_root(blok):
    level = [H(b) for b in blok]
    while len(level) > 1:
        level = level_atas(level)
    return level[0]


def merkle_proof(blok, idx):
    """List (hash saudara, saudara_di_kiri) dari leaf ke akar."""
    level, bukti = [H(b) for b in blok], []
    while len(level) > 1:
        if len(level) % 2 == 1:
            level = level + [level[-1]]
        saudara = idx ^ 1
        bukti.append((level[saudara], saudara < idx))
        level, idx = level_atas(level), idx // 2
    return bukti


def verify(data, bukti, akar):
    h = H(data)
    for s, di_kiri in bukti:
        h = H(s + h) if di_kiri else H(h + s)
    return h == akar


if __name__ == "__main__":
    blok = [b"blok-%d" % i for i in range(8)]
    akar = merkle_root(blok)
    for i in range(8):
        bukti = merkle_proof(blok, i)
        assert len(bukti) == 3                      # log2(8)
        assert verify(blok[i], bukti, akar)
    palsu = merkle_proof(blok, 5)
    assert not verify(b"blok-5 diubah", palsu, akar)

    ganjil = [b"a", b"b", b"c", b"d", b"e"]
    r = merkle_root(ganjil)
    for i in range(5):
        assert verify(ganjil[i], merkle_proof(ganjil, i), r)

    # dua replica membandingkan akar dulu; turun hanya ke cabang yang beda
    replica = blok[:]
    replica[6] = b"blok-6 versi lain"
    assert merkle_root(replica) != akar
    kiri_sama = merkle_root(blok[:4]) == merkle_root(replica[:4])
    kanan_sama = merkle_root(blok[4:]) == merkle_root(replica[4:])
    assert kiri_sama and not kanan_sama
    print("akar:", akar.hex()[:16], "...")
    print("merkle: semua uji lolos")
