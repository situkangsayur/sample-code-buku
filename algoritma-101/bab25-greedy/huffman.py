"""Huffman coding dengan heapq (Algoritma 25.4, Kode 25.2)."""
import heapq
from itertools import count


def huffman(frek):
    """frek: dict simbol -> frekuensi. Mengembalikan dict simbol -> kode bit.
    Penghitung urutan dipakai sebagai pemecah seri agar hasilnya tetap."""
    urutan = count()
    heap = [(f, next(urutan), s) for s, f in sorted(frek.items())]
    heapq.heapify(heap)
    if len(heap) == 1:
        return {heap[0][2]: "0"}
    while len(heap) > 1:
        f1, _, kiri = heapq.heappop(heap)     # dua frekuensi terkecil
        f2, _, kanan = heapq.heappop(heap)
        heapq.heappush(heap, (f1 + f2, next(urutan), (kiri, kanan)))
    kode = {}

    def jalan(t, awalan):
        if isinstance(t, tuple):
            jalan(t[0], awalan + "0")
            jalan(t[1], awalan + "1")
        else:
            kode[t] = awalan

    jalan(heap[0][2], "")
    return kode


def frekuensi(teks):
    f = {}
    for c in teks:
        f[c] = f.get(c, 0) + 1
    return f


if __name__ == "__main__":
    teks = "ABRAKADABRA"
    f = frekuensi(teks)
    assert f == {"A": 5, "B": 2, "R": 2, "K": 1, "D": 1}
    kode = huffman(f)
    total = sum(len(kode[c]) for c in teks)
    assert total == 23                        # vs 11 x 3 = 33 bit kode tetap
    assert len(kode["A"]) == 1
    # prefix-free: tidak ada kode yang menjadi awalan kode lain
    ks = list(kode.values())
    assert not any(a != b and b.startswith(a) for a in ks for b in ks)
    # decode kembali
    balik = {v: k for k, v in kode.items()}
    bit = "".join(kode[c] for c in teks)
    hasil, buf = "", ""
    for b in bit:
        buf += b
        if buf in balik:
            hasil += balik[buf]
            buf = ""
    assert hasil == teks
    print("kode:", dict(sorted(kode.items())), "total bit:", total)
    print("huffman.py: semua uji lolos")
