"""Bab 36: dua tahap DEFLATE secara sederhana, LZ77 lalu Huffman.

LZ77 mengganti pengulangan dengan pasangan (jarak, panjang) ke belakang.
Huffman (greedy, Bab 25) memberi kode pendek untuk simbol yang sering.
Hasil dibandingkan dengan zlib (DEFLATE asli) dan, bila ada, zstd.
"""
import heapq
import shutil
import subprocess
import zlib
from collections import Counter

WINDOW, MIN_MATCH, MAX_MATCH = 32768, 3, 258     # angka DEFLATE (RFC 1951)


def lz77_encode(data):
    """Token: ("lit", byte) atau ("ref", jarak, panjang). Pencarian naif."""
    token, i, posisi = [], 0, {}
    while i < len(data):
        terbaik = (0, 0)
        for j in reversed(posisi.get(data[i:i + MIN_MATCH], [])):
            if i - j > WINDOW:
                break
            n = 0
            while n < MAX_MATCH and i + n < len(data) and data[j + n] == data[i + n]:
                n += 1
            if n > terbaik[1]:
                terbaik = (i - j, n)
        langkah = terbaik[1] if terbaik[1] >= MIN_MATCH else 1
        token.append(("ref",) + terbaik if langkah > 1 else ("lit", data[i]))
        for p in range(i, i + langkah):
            posisi.setdefault(data[p:p + MIN_MATCH], []).append(p)
        i += langkah
    return token


def lz77_decode(token):
    out = bytearray()
    for t in token:
        if t[0] == "lit":
            out.append(t[1])
        else:
            _, jarak, panjang = t
            for _ in range(panjang):             # boleh tumpang tindih
                out.append(out[-jarak])
    return bytes(out)


def huffman_panjang_kode(frek):
    """Panjang kode Huffman per simbol (greedy: gabung dua terkecil)."""
    if len(frek) == 1:
        return {s: 1 for s in frek}
    heap = [(f, i, {s: 0}) for i, (s, f) in enumerate(frek.items())]
    heapq.heapify(heap)
    urut = len(heap)
    while len(heap) > 1:
        f1, _, a = heapq.heappop(heap)
        f2, _, b = heapq.heappop(heap)
        gabung = {s: d + 1 for s, d in {**a, **b}.items()}
        heapq.heappush(heap, (f1 + f2, urut, gabung))
        urut += 1
    return heap[0][2]


if __name__ == "__main__":
    teks = b"abrakadabra abrakadabra abrakadabra!"
    tok = lz77_encode(teks)
    assert lz77_decode(tok) == teks
    print(tok[:12])
    assert ("ref", 12, 23) in tok                     # dua salinan terakhir sekaligus

    frek = Counter(b"abrakadabra")                   # a:5 b:2 r:2 k:1 d:1
    pk = huffman_panjang_kode(frek)
    total = sum(frek[s] * pk[s] for s in frek)
    print({chr(s): pk[s] for s in pk}, "total bit =", total)
    assert total == 23 and pk[ord("a")] == 1

    data = b"".join(b"%d,mahasiswa-%d,TI,3.%d\n" % (i, i, i % 10) for i in range(2000))
    assert lz77_decode(lz77_encode(data[:4000])) == data[:4000]
    z = zlib.compress(data, 9)
    assert zlib.decompress(z) == data
    print("data %d byte, zlib-9 %d byte (rasio %.1f)" % (len(data), len(z), len(data) / len(z)))
    if shutil.which("zstd"):
        hasil = subprocess.run(["zstd", "-19", "-c", "-q"], input=data,
                               capture_output=True, check=True).stdout
        balik = subprocess.run(["zstd", "-d", "-c", "-q"], input=hasil,
                               capture_output=True, check=True).stdout
        assert balik == data
        print("zstd-19 %d byte" % len(hasil))
    print("lz77_huffman: semua uji lolos")
