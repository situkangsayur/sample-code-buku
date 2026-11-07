"""Memeriksa contoh temperature dan top-p pada Bab 14 (Gambar 14.2) dengan NumPy."""
import numpy as np

token = ["nasi", "roti", "mie", "batu"]
logit = np.array([2.0, 1.0, 0.5, -1.0])


def softmax_suhu(z, T):
    z = z / T
    e = np.exp(z - z.max())
    return e / e.sum()


def top_p(p, ambang):
    urut = np.argsort(-p)
    kumulatif = np.cumsum(p[urut])
    n = int(np.searchsorted(kumulatif, ambang) + 1)   # himpunan terkecil >= ambang
    pilih = urut[:n]
    return {token[i]: round(float(p[i] / p[pilih].sum()), 3) for i in pilih}


for T in [0.25, 0.5, 1.0, 2.0]:
    p = softmax_suhu(logit, T)
    print(f"T={T:4}:", dict(zip(token, np.round(p, 3))), " top-p 0.8:", top_p(p, 0.8))

rng = np.random.default_rng(0)
p = softmax_suhu(logit, 1.0)
sampel = rng.choice(token, size=1000, p=p)
print("frekuensi 1000 sampel T=1:", {t: int((sampel == t).sum()) for t in token})
