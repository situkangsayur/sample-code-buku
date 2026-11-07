"""Diagnostik regresi: residual dan VIF untuk multikolinearitas (Bab 10, Kode 10.8)."""
import numpy as np
from sklearn.linear_model import LinearRegression

rng = np.random.default_rng(0)
n = 200
luas_m2 = rng.uniform(30, 200, n)
kamar = np.round(luas_m2 / 35 + rng.normal(0, 0.6, n))       # berkorelasi dengan luas
umur = rng.uniform(0, 30, n)
luas_ft2 = luas_m2 * 10.7639 + rng.normal(0, 5, n)            # hampir duplikat luas_m2
X = np.c_[luas_m2, kamar, umur, luas_ft2]
nama = ["luas_m2", "kamar", "umur", "luas_ft2"]
harga = 8 * luas_m2 + 20 * kamar - 3 * umur + rng.normal(0, 60, n)  # juta rupiah


def vif(X):
    """VIF_j = 1 / (1 - R_j^2), R_j^2 dari regresi fitur j atas fitur lain."""
    hasil = []
    for j in range(X.shape[1]):
        lain = np.delete(X, j, axis=1)
        r2 = LinearRegression().fit(lain, X[:, j]).score(lain, X[:, j])
        hasil.append(1 / (1 - r2))
    return hasil


for nm, v in zip(nama, vif(X)):
    print(f"VIF {nm:9s} = {v:8.1f}")
model = LinearRegression().fit(X, harga)
print("koefisien:", dict(zip(nama, model.coef_.round(2))))
residual = harga - model.predict(X)
print("rata-rata residual:", round(residual.mean(), 6))
