"""Kode 8.4: median, speedup, efisiensi, Karp-Flatt, dan kurva Amdahl.
Pemakaian: python olah.py hasil.csv
"""
import csv
import statistics as st
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

berkas = sys.argv[1] if len(sys.argv) > 1 else "hasil.csv"
data, hasil_prima = {}, set()
for p, t, n in csv.reader(open(berkas)):
    data.setdefault(int(p), []).append(float(t))
    hasil_prima.add(n)
if len(hasil_prima) != 1:
    sys.exit(f"PERINGATAN: jumlah prima berbeda antar-run: {hasil_prima}")

P = sorted(data)
T = {p: st.median(data[p]) for p in P}
S = {p: T[1] / T[p] for p in P}
e = [(1 / S[p] - 1 / p) / (1 - 1 / p) for p in P if p > 1]
f = st.median(e) if e else 0.0           # fraksi serial taksiran
for p in P:
    kf = (1 / S[p] - 1 / p) / (1 - 1 / p) if p > 1 else float("nan")
    print(f"p={p:3d} T={T[p]:8.3f} S={S[p]:6.2f} E={S[p]/p:5.0%} e={kf:6.3f}")
print(f"taksiran f = {f:.4f}, batas speedup ~ {1/f if f > 0 else float('inf'):.1f}")

plt.plot(P, [S[p] for p in P], "o-", label="terukur")
plt.plot(P, [1 / (f + (1 - f) / p) for p in P], "--", label=f"Amdahl f={f:.3f}")
plt.plot(P, P, ":", label="ideal")
plt.xlabel("p"); plt.ylabel("speedup"); plt.legend()
plt.savefig("speedup.png", dpi=150)
print("grafik disimpan ke speedup.png")
