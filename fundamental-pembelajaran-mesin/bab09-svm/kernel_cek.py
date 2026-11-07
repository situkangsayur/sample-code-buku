"""Memeriksa kernel trick: (x.z)^2 sama dengan phi(x).phi(z) (Bab 9, Kode 9.2)."""
import numpy as np


def phi(v):
    """Pemetaan eksplisit untuk kernel polinomial derajat 2 tanpa konstanta."""
    return np.array([v[0] ** 2, np.sqrt(2) * v[0] * v[1], v[1] ** 2])


def rbf(x, z, gamma):
    return np.exp(-gamma * np.sum((x - z) ** 2))


x, z = np.array([1.0, 2.0]), np.array([3.0, 1.0])
print("kernel  :", (x @ z) ** 2)          # 25
print("eksplisit:", phi(x) @ phi(z))       # 25
for g in (0.01, 0.1, 1, 10):               # dua titik berjarak kuadrat 4
    print(g, rbf(np.zeros(2), np.array([2.0, 0.0]), g))
