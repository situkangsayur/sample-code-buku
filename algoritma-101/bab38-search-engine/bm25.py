"""Bab 38: TF-IDF dan BM25.

BM25 (bentuk Lucene, BM25Similarity):
    idf(t)     = ln(1 + (N - n_t + 0,5) / (n_t + 0,5))
    skor(t, d) = idf(t) * f / (f + k1 * (1 - b + b * |d| / avgdl))
Bentuk klasik mengalikan pembilang dengan (k1 + 1); konstanta itu tidak
mengubah urutan hasil. Default Lucene: k1 = 1,2 dan b = 0,75.
"""
import math

from inverted_index import DOKUMEN, analyzer, bangun_index


class BM25:
    def __init__(self, dokumen, k1=1.2, b=0.75, klasik=False):
        self.index = bangun_index(dokumen)
        self.panjang = [len(analyzer(d)) for d in dokumen]
        self.N = len(dokumen)
        self.avgdl = sum(self.panjang) / self.N
        self.k1, self.b, self.klasik = k1, b, klasik

    def idf(self, term):
        n = len(self.index.get(term, []))
        return math.log(1 + (self.N - n + 0.5) / (n + 0.5))

    def skor_term(self, term, doc_id, f):
        norm = self.k1 * (1 - self.b + self.b * self.panjang[doc_id] / self.avgdl)
        tf = f / (f + norm)
        if self.klasik:
            tf *= self.k1 + 1
        return self.idf(term) * tf

    def cari(self, query, top=3):
        skor = {}
        for _, term in analyzer(query):
            for doc_id, posisi in self.index.get(term, []):   # hanya posting list
                skor[doc_id] = skor.get(doc_id, 0.0) + self.skor_term(term, doc_id, len(posisi))
        return sorted(skor.items(), key=lambda x: (-x[1], x[0]))[:top]


def tfidf(dokumen, query):
    """tf * log(N / df), tanpa normalisasi panjang (pembanding)."""
    index = bangun_index(dokumen)
    N, skor = len(dokumen), {}
    for _, term in analyzer(query):
        posting = index.get(term, [])
        for doc_id, posisi in posting:
            skor[doc_id] = skor.get(doc_id, 0.0) + len(posisi) * math.log(N / len(posting))
    return sorted(skor.items(), key=lambda x: (-x[1], x[0]))


if __name__ == "__main__":
    m = BM25(DOKUMEN)
    assert m.panjang == [4, 4, 5, 6, 5] and m.avgdl == 4.8
    # contoh di buku: term "bm25" hanya di dokumen 3
    assert abs(m.idf("bm25") - math.log(1 + 4.5 / 1.5)) < 1e-12          # ln 4
    assert abs(m.idf("index") - math.log(1 + 1.5 / 4.5)) < 1e-12         # ln(4/3)
    s = m.skor_term("bm25", 3, 1)
    norm = 1.2 * (0.25 + 0.75 * 6 / 4.8)
    assert abs(s - math.log(4) * 1 / (1 + norm)) < 1e-12
    print("idf(bm25) = %.4f, norm = %.4f, skor = %.4f" % (m.idf("bm25"), norm, s))

    hasil = m.cari("inverted index bm25")
    print("BM25  :", [(d, round(x, 4)) for d, x in hasil])
    assert hasil[0][0] == 3
    klasik = BM25(DOKUMEN, klasik=True).cari("inverted index bm25")
    assert [d for d, _ in klasik] == [d for d, _ in hasil]               # urutan sama

    # f naik, skor jenuh menuju idf: beda dengan tf-idf yang linear
    nilai = [m.skor_term("bm25", 3, f) for f in (1, 2, 4, 8, 100)]
    assert all(a < b for a, b in zip(nilai, nilai[1:])) and nilai[-1] < m.idf("bm25")
    print("TF-IDF:", [(d, round(x, 4)) for d, x in tfidf(DOKUMEN, "inverted index bm25")])
    print("bm25: semua uji lolos")
