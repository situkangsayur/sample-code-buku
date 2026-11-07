"""POS tagging bahasa Indonesia dengan HMM (latih dengan menghitung, decode dengan Viterbi).

Korpus mini buatan sendiri untuk ilustrasi; tag mengikuti sebagian tagset
Dinakaramani dkk. (2014): NN nomina, NNP nama diri, PRP pronomina persona,
PR pronomina penunjuk, VB verba, MD modal, JJ adjektiva, IN preposisi,
NEG negasi, CD bilangan.
Untuk penelitian, pakai korpus beranotasi berukuran besar.
"""
from collections import Counter, defaultdict
import numpy as np
from hmm_numpy import viterbi_log

KORPUS = """saya/PRP bisa/MD membaca/VB buku/NN itu/PR
dia/PRP bisa/MD berenang/VB di/IN kolam/NN
ular/NN itu/PR punya/VB bisa/NN yang/SC kuat/JJ
bisa/NN ular/NN kobra/NN sangat/RB berbahaya/JJ
kami/PRP tidak/NEG bisa/MD datang/VB besok/NN
budi/NNP membaca/VB buku/NN baru/JJ
ani/NNP membeli/VB dua/CD buku/NN di/IN pasar/NN
anak/NN itu/PR tidak/NEG punya/VB buku/NN
racun/NN itu/PR sangat/RB kuat/JJ
mereka/PRP punya/VB kolam/NN yang/SC besar/JJ
ibu/NN bisa/MD memasak/VB rendang/NN
ular/NN itu/PR tidak/NEG berbahaya/JJ"""


def baca(korpus):
    return [[tuple(tok.split("/")) for tok in baris.split()] for baris in korpus.splitlines()]


def latih(kalimat, k=0.1):
    """Taksiran maximum likelihood dengan add-k smoothing."""
    tags = sorted({t for s in kalimat for _, t in s})
    kata = sorted({w for s in kalimat for w, _ in s}) + ["<unk>"]
    ti = {t: i for i, t in enumerate(tags)}; wi = {w: i for i, w in enumerate(kata)}
    N, M = len(tags), len(kata)
    pi = np.full(N, k); A = np.full((N, N), k); B = np.full((N, M), k)
    for s in kalimat:
        pi[ti[s[0][1]]] += 1
        for (w, t) in s:
            B[ti[t], wi[w]] += 1
        for (_, t1), (_, t2) in zip(s, s[1:]):
            A[ti[t1], ti[t2]] += 1
    return (A / A.sum(1, keepdims=True), B / B.sum(1, keepdims=True),
            pi / pi.sum(), tags, wi)


def tag(kalimat, A, B, pi, tags, wi):
    O = np.array([wi.get(w, wi["<unk>"]) for w in kalimat.split()])
    q, lp = viterbi_log(A, B, pi, O)
    return [(w, tags[i]) for w, i in zip(kalimat.split(), q)], lp


if __name__ == "__main__":
    data = baca(KORPUS)
    A, B, pi, tags, wi = latih(data)
    print("tag:", tags)
    print(f"jumlah kalimat {len(data)}, token {sum(map(len, data))}, kosakata {len(wi) - 1}")
    i_md, i_nn, w = tags.index("MD"), tags.index("NN"), wi["bisa"]
    print(f"P(bisa|MD) = {B[i_md, w]:.3f}, P(bisa|NN) = {B[i_nn, w]:.3f}")
    for a in ("PR", "PRP", "VB"):
        print(f"P(MD|{a}) = {A[tags.index(a), i_md]:.3f}, P(NN|{a}) = {A[tags.index(a), i_nn]:.3f}")
    for s in ("adik bisa membaca buku itu", "racun ular itu punya bisa",
              "kobra punya bisa yang berbahaya"):
        hasil, lp = tag(s, A, B, pi, tags, wi)
        print(" ".join(f"{w}/{t}" for w, t in hasil), f"  (log P = {lp:.2f})")
