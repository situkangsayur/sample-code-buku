"""Deteksi anomali dengan densitas GMM (Bab 6)."""
import numpy as np
from sklearn.mixture import GaussianMixture
from data_nasabah import buat_data

X, _ = buat_data()
gmm = GaussianMixture(3, covariance_type="full", tol=1e-6, max_iter=500,
                      n_init=5, random_state=0).fit(X)

skor = gmm.score_samples(X)              # log p(x) setiap nasabah
ambang = np.percentile(skor, 1)          # 1% terendah dianggap janggal
print(f"ambang log p(x) (persentil 1): {ambang:.3f}")
print(f"nasabah latih di bawah ambang : {(skor < ambang).sum()}")

uji = np.array([[6.8, 18.0],    # tipikal segmen karyawan
                [5.5, 70.0],    # saldo kecil, transaksi sangat banyak
                [8.3, 40.0],    # saldo sangat besar, transaksi banyak
                [6.3, 26.0]])   # di antara dua segmen, tetapi masih wajar
for u, s in zip(uji, gmm.score_samples(uji)):
    status = "ANOMALI" if s < ambang else "normal"
    print(f"{u}: log p(x) = {s:8.3f} -> {status}")
