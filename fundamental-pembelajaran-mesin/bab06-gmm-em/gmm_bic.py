"""Memilih jumlah komponen dan bentuk kovarians dengan BIC dan AIC (Bab 6)."""
import numpy as np
from sklearn.mixture import GaussianMixture
from data_nasabah import buat_data

X, _ = buat_data()
hasil = {}
for cov in ["full", "tied", "diag", "spherical"]:
    for K in range(1, 7):
        g = GaussianMixture(K, covariance_type=cov, tol=1e-6, max_iter=500,
                            n_init=5, random_state=0).fit(X)
        hasil[cov, K] = (g.bic(X), g.aic(X), g._n_parameters())

print("BIC (makin kecil makin baik)")
print("K   " + "".join(f"{c:>11s}" for c in ["full", "tied", "diag", "spherical"]))
for K in range(1, 7):
    print(f"{K}   " + "".join(f"{hasil[c, K][0]:11.1f}"
                            for c in ["full", "tied", "diag", "spherical"]))
terbaik = min(hasil, key=lambda k: hasil[k][0])
print("terbaik menurut BIC:", terbaik, f"BIC = {hasil[terbaik][0]:.1f}")
print("\nfull: K, banyak parameter, BIC, AIC")
for K in range(1, 7):
    b, a, p = hasil["full", K]
    print(f"  K={K}: p={p:2d}  BIC={b:8.1f}  AIC={a:8.1f}")
