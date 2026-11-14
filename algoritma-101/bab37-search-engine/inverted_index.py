"""Bab 37: analyzer sederhana, inverted index dengan posisi, dan query.

analyzer: lowercase -> tokenization (huruf/angka) -> buang stopword.
posting list: term -> list (doc_id, [posisi]) terurut menurut doc_id.
AND query = irisan posting list (two pointer); phrase query memakai posisi.
"""
import re

STOPWORD = {"dan", "di", "ke", "dari", "yang", "untuk", "pada", "dengan", "adalah", "the"}


def analyzer(teks):
    """Kembalikan list (posisi, term). Posisi dihitung sebelum stopword dibuang."""
    token = re.findall(r"[0-9a-z]+", teks.lower())
    return [(i, t) for i, t in enumerate(token) if t not in STOPWORD]


def bangun_index(dokumen):
    index = {}
    for doc_id, teks in enumerate(dokumen):          # doc_id naik: list tetap terurut
        for pos, term in analyzer(teks):
            posting = index.setdefault(term, [])
            if posting and posting[-1][0] == doc_id:
                posting[-1][1].append(pos)
            else:
                posting.append((doc_id, [pos]))
    return index


def irisan(p1, p2):
    """Irisan dua posting list terurut: O(|p1| + |p2|)."""
    hasil, i, j = [], 0, 0
    while i < len(p1) and j < len(p2):
        if p1[i][0] == p2[j][0]:
            hasil.append(p1[i][0])
            i += 1
            j += 1
        elif p1[i][0] < p2[j][0]:
            i += 1
        else:
            j += 1
    return hasil


def cari_and(index, query):
    terms = [t for _, t in analyzer(query)]
    if not terms:
        return []
    lists = sorted((index.get(t, []) for t in terms), key=len)   # terpendek dulu
    hasil = [d for d, _ in lists[0]]
    for p in lists[1:]:
        hasil = irisan([(d, None) for d in hasil], p)
    return hasil


def cari_frasa(index, frasa):
    """Dokumen yang memuat term berurutan pada posisi berurutan."""
    terms = analyzer(frasa)
    if not terms:
        return []
    awal_pos = terms[0][0]
    calon = set(cari_and(index, frasa))
    hasil = []
    for d in sorted(calon):
        pos = {t: set(dict(index[t])[d]) for _, t in terms}
        p0 = pos[terms[0][1]]
        if any(all(p + (q - awal_pos) in pos[t] for q, t in terms) for p in p0):
            hasil.append(d)
    return hasil


DOKUMEN = [
    "Binary search pada array terurut",
    "B-tree adalah index di database",
    "Inverted index dipakai search engine",
    "Search engine memakai inverted index dan BM25",
    "Index database dan search engine berbeda",
]

if __name__ == "__main__":
    assert analyzer("Search Engine, dan BM25!") == [(0, "search"), (1, "engine"), (3, "bm25")]
    idx = bangun_index(DOKUMEN)
    assert idx["index"] == [(1, [3]), (2, [1]), (3, [4]), (4, [0])]
    assert idx["search"] == [(0, [1]), (2, [3]), (3, [0]), (4, [3])]
    assert irisan(idx["index"], idx["search"]) == [2, 3, 4]
    assert cari_and(idx, "search engine index") == [2, 3, 4]
    assert cari_frasa(idx, "inverted index") == [2, 3]
    assert cari_frasa(idx, "index database") == [4]
    assert cari_and(idx, "kuantum") == []
    for term in sorted(idx):
        print("%-10s %s" % (term, idx[term]))
    print("inverted_index: semua uji lolos")
