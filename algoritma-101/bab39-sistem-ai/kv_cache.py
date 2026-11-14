"""Bab 39: KV cache pada decoding transformer, dihitung dari sudut banyak operasi.

Satu head attention kecil (d = 4) dengan bobot tetap. Kita bandingkan
generasi n token tanpa cache (K dan V seluruh prefix dihitung ulang) dan dengan
cache (hanya K dan V token baru yang dihitung). Keluarannya harus sama.
Jalankan: python3 kv_cache.py
"""
import math

D = 4


def matrix(seed):
    # bobot deterministik kecil supaya hasil dapat diulang di Python dan Rust
    return [[math.sin(seed + 3 * i + j) / 2 for j in range(D)] for i in range(D)]


WQ, WK, WV = matrix(1), matrix(2), matrix(3)


class Counter:
    def __init__(self):
        self.proj = 0     # perkalian untuk proyeksi K dan V
        self.attn = 0     # perkalian untuk skor q.k dan jumlah berbobot


def matvec(w, x, ctr=None):
    if ctr is not None:
        ctr.proj += D * D
    return [sum(w[i][j] * x[j] for j in range(D)) for i in range(D)]


def attend(q, keys, values, ctr):
    scores = []
    for k in keys:
        ctr.attn += D
        scores.append(sum(a * b for a, b in zip(q, k)) / math.sqrt(D))
    mx = max(scores)
    ex = [math.exp(s - mx) for s in scores]
    tot = sum(ex)
    out = [0.0] * D
    for e, v in zip(ex, values):
        ctr.attn += D
        for i in range(D):
            out[i] += e / tot * v[i]
    return out


def embed(t):
    return [math.cos(t + i) for i in range(D)]


def generate(n, use_cache):
    ctr = Counter()
    xs = [embed(0)]
    cache_k, cache_v = [], []
    outputs = []
    for step in range(n):
        x = xs[-1]
        q = matvec(WQ, x)
        if use_cache:
            cache_k.append(matvec(WK, x, ctr))   # hanya token baru
            cache_v.append(matvec(WV, x, ctr))
            keys, values = cache_k, cache_v
        else:
            keys = [matvec(WK, xi, ctr) for xi in xs]   # seluruh prefix dihitung ulang
            values = [matvec(WV, xi, ctr) for xi in xs]
        y = attend(q, keys, values, ctr)
        outputs.append(y)
        xs.append([a + b for a, b in zip(embed(step + 1), y)])  # token berikutnya
    return outputs, ctr


def kv_bytes_per_token(layers, hidden, bytes_per_value):
    """2 (K dan V) x hidden x layers x byte per nilai."""
    return 2 * hidden * layers * bytes_per_value


if __name__ == "__main__":
    print("   n  proj_tanpa  proj_cache  attn")
    for n in (8, 64, 512):
        o1, c1 = generate(n, use_cache=False)
        o2, c2 = generate(n, use_cache=True)
        assert all(abs(a - b) < 1e-12 for y1, y2 in zip(o1, o2) for a, b in zip(y1, y2))
        assert c1.proj == 2 * D * D * n * (n + 1) // 2   # Theta(n^2)
        assert c2.proj == 2 * D * D * n                  # Theta(n)
        assert c1.attn == c2.attn == 2 * D * n * (n + 1) // 2
        print(f"{n:4d}  {c1.proj:10d}  {c2.proj:10d}  {c2.attn:6d}")

    # angka dari makalah PagedAttention (Kwon dkk. 2023) untuk OPT-13B
    b = kv_bytes_per_token(layers=40, hidden=5120, bytes_per_value=2)
    assert b == 819_200
    print(f"OPT-13B: {b} byte per token = {b / 1024:.0f} KiB; 2048 token = {b * 2048 / 2**30:.2f} GiB")
    print("semua uji kv_cache lolos")
