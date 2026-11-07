"""EM untuk campuran Bernoulli pada data biner kecil (Bab 6; Bishop 2006, Subbab 9.3.3).

Setiap baris adalah satu nasabah, setiap kolom memakai (1) atau tidak (0) satu layanan:
  QRIS, e-wallet top-up, deposito, reksa dana.
"""
import numpy as np

X = np.array([[1, 1, 0, 0],
              [1, 1, 0, 0],
              [1, 1, 1, 0],
              [1, 0, 0, 0],
              [0, 0, 1, 1],
              [0, 1, 1, 1],
              [0, 0, 1, 1],
              [1, 0, 1, 1]], dtype=float)
N, D = X.shape
K = 2
pi = np.array([0.5, 0.5])
mu = np.array([[0.6, 0.5, 0.4, 0.5],      # inisialisasi sedikit tidak simetris
               [0.4, 0.5, 0.6, 0.5]])

def log_bern(X, mu):
    # log p(x_n | mu_k) = sum_i x_ni log mu_ki + (1 - x_ni) log(1 - mu_ki)
    return X @ np.log(mu).T + (1 - X) @ np.log(1 - mu).T   # N x K

np.set_printoptions(precision=3, suppress=True)
for it in range(1, 51):
    log_p = np.log(pi) + log_bern(X, mu)                    # E-step
    log_px = np.logaddexp.reduce(log_p, axis=1)
    gamma = np.exp(log_p - log_px[:, None])
    Nk = gamma.sum(axis=0)                                  # M-step
    pi = Nk / N
    mu = (gamma.T @ X) / Nk[:, None]
    mu = np.clip(mu, 1e-3, 1 - 1e-3)                        # cegah log(0)
    if it == 1:
        print("iterasi 1, gamma(z_n1):", gamma[:, 0])
        print("iterasi 1, mu:\n", mu)
    if it > 1 and log_px.sum() - ll_lama < 1e-8:
        break
    ll_lama = log_px.sum()
print(f"konvergen setelah {it} iterasi, logL = {log_px.sum():.3f}")
print("pi:", pi)
print("mu:\n", mu)
print("gamma(z_n1):", gamma[:, 0])
