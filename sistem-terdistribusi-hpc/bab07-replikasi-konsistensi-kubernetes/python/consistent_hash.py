"""Kode 7.3: consistent hashing dengan virtual node, dibandingkan hash mod N.

Pemakaian: python consistent_hash.py
"""
import bisect, hashlib
from collections import Counter


def h(s: str) -> int:
    return int.from_bytes(hashlib.sha256(s.encode()).digest()[:8], "big")


class Cincin:
    def __init__(self, mesin, vnode=100):
        self.titik = sorted((h(f"{m}#{i}"), m) for m in mesin for i in range(vnode))
        self.kunci = [t for t, _ in self.titik]

    def pemilik(self, key: str) -> str:
        i = bisect.bisect(self.kunci, h(key)) % len(self.titik)  # titik berikutnya
        return self.titik[i][1]


def mod_n(key, mesin):
    return mesin[h(key) % len(mesin)]


if __name__ == "__main__":
    keys = [f"pesanan-{i}" for i in range(100_000)]
    m4, m5 = ["A", "B", "C", "D"], ["A", "B", "C", "D", "E"]
    pindah = sum(mod_n(k, m4) != mod_n(k, m5) for k in keys)
    print(f"hash mod N      : key pindah {pindah / len(keys):6.1%}")
    for v in (1, 10, 100):
        lama, baru = Cincin(m4, v), Cincin(m5, v)
        pindah = sum(lama.pemilik(k) != baru.pemilik(k) for k in keys)
        beban = Counter(baru.pemilik(k) for k in keys)
        rentang = (min(beban.values()) / len(keys), max(beban.values()) / len(keys))
        print(f"consistent v={v:3d}: key pindah {pindah / len(keys):6.1%}, "
              f"beban per mesin {rentang[0]:.1%}..{rentang[1]:.1%}")
