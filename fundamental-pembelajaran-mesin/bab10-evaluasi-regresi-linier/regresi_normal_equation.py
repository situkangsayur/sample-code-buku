"""Regresi linier dengan normal equation, R^2, standard error (Bab 10, Kode 10.6)."""
import numpy as np

x = np.array([1, 2, 3, 4, 5], dtype=float)   # jam belajar per minggu
y = np.array([2, 4, 5, 4, 5], dtype=float)   # nilai kuis

X = np.c_[np.ones_like(x), x]                # kolom konstanta untuk beta_0
beta = np.linalg.solve(X.T @ X, X.T @ y)     # selesaikan X'X beta = X'y, jangan invers
print("beta =", beta)                         # [2.2 0.6]

beta_lstsq, *_ = np.linalg.lstsq(X, y, rcond=None)   # cara yang lebih stabil (QR/SVD)
print("lstsq =", beta_lstsq)

y_hat = X @ beta
e = y - y_hat
rss, tss = e @ e, ((y - y.mean()) ** 2).sum()
n, p = len(y), X.shape[1] - 1
r2 = 1 - rss / tss
r2_adj = 1 - (1 - r2) * (n - 1) / (n - p - 1)
print(f"RSS={rss:.2f} RMSE={np.sqrt(rss / n):.3f} R2={r2:.2f} R2_adj={r2_adj:.2f}")

# Standard error koefisien: sigma^2 (X'X)^-1, sigma^2 = RSS/(n-p-1)
sigma2 = rss / (n - p - 1)
se = np.sqrt(np.diag(sigma2 * np.linalg.inv(X.T @ X)))
print("SE =", se.round(3), " t(beta_1) =", round(beta[1] / se[1], 2))
