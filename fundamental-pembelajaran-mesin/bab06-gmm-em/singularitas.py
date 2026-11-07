"""Singularitas pada MLE campuran Gaussian dan efek reg_covar (Bab 6).

Komponen 2 diletakkan tepat di atas satu titik data (x = 1) lalu sigma-nya
dikecilkan: log-likelihood naik tanpa batas.
"""
import numpy as np

x = np.array([1.0, 2.0, 3.0, 6.0, 7.0, 8.0])


def logL(x, pi, mu, sd):
    dens = np.exp(-(x[:, None] - mu) ** 2 / (2 * sd ** 2)) / (np.sqrt(2 * np.pi) * sd)
    return np.log((pi * dens).sum(axis=1)).sum()


pi = np.array([0.5, 0.5])
for sd2 in [1.0, 1e-2, 1e-4, 1e-8, 1e-16]:
    mu = np.array([x.mean(), 1.0])
    sd = np.array([x.std(), np.sqrt(sd2)])
    print(f"varians komponen 2 = {sd2:8.0e}: logL = {logL(x, pi, mu, sd):8.3f}")

# Dengan reg_covar, varians tidak pernah di bawah reg_covar
reg = 1e-2
sd = np.array([x.std(), np.sqrt(1e-8 + reg)])
print(f"dengan reg_covar = {reg}: logL = {logL(x, pi, np.array([x.mean(), 1.0]), sd):8.3f}")
