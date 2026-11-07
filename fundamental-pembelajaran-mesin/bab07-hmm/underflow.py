"""Underflow pada forward polos dan solusinya (scaling, log-space)."""
import math
import numpy as np
from hmm_numpy import forward, forward_scaled, sample

A = np.array([[0.8, 0.2], [0.3, 0.7]])
B = np.array([[0.3, 0.6, 0.1], [0.4, 0.1, 0.5]])
pi = np.array([0.6, 0.4])

print("Bilangan float64 positif terkecil (normal):", np.finfo(float).tiny)
rng = np.random.default_rng(42)
_, O = sample(A, B, pi, 2000, rng)
for T in (10, 100, 500, 1000, 2000):
    _, p = forward(A, B, pi, O[:T])
    _, c, ll = forward_scaled(A, B, pi, O[:T])
    print(f"T={T:5d}  forward polos P(O)={p:.3e}   berskala log P(O)={ll:.4f}"
          f"   log10 P(O)={ll / math.log(10):.2f}")

# Ongkos hitung: enumerasi naif ~ 2T N^T, forward ~ N^2 T
for N, T in ((2, 3), (5, 100), (45, 20)):
    naif = 2 * T * N**T
    print(f"N={N:2d} T={T:3d}: naif ~ {naif:.2e} operasi, forward ~ {N*N*T:,} operasi")

# Langkah pertama alpha polos jatuh di bawah tiny (subnormal) dan menjadi nol
alpha, _ = forward(A, B, pi, O[:1000])
s = alpha.sum(axis=1)
print("alpha < tiny mulai t =", np.argmax(s < np.finfo(float).tiny) + 1,
      "; alpha = 0 mulai t =", np.argmax(s == 0) + 1)
