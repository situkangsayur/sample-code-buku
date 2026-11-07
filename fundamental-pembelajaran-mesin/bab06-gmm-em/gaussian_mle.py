"""MLE satu Gaussian multivariat dan log-likelihood-nya (Bab 6)."""
import numpy as np
from data_nasabah import buat_data


def log_gauss(X, mu, Sigma):
    """log N(x | mu, Sigma) untuk setiap baris X, lewat dekomposisi Cholesky."""
    d = X.shape[1]
    L = np.linalg.cholesky(Sigma)                 # Sigma = L L^T
    z = np.linalg.solve(L, (X - mu).T)            # z = L^{-1}(x - mu)
    mahal2 = (z ** 2).sum(axis=0)                 # jarak Mahalanobis kuadrat
    log_det = 2 * np.log(np.diag(L)).sum()        # log |Sigma|
    return -0.5 * (d * np.log(2 * np.pi) + log_det + mahal2)


if __name__ == "__main__":
    X, _ = buat_data()
    n = len(X)
    mu_hat = X.mean(axis=0)                           # MLE rata-rata
    Sigma_hat = (X - mu_hat).T @ (X - mu_hat) / n     # MLE kovarians (bagi n)
    ll = log_gauss(X, mu_hat, Sigma_hat).sum()
    print("mu_hat   :", mu_hat.round(3))
    print("Sigma_hat:\n", Sigma_hat.round(3))
    print(f"log-likelihood satu Gaussian: {ll:.2f}")
    print(f"rata-rata per nasabah       : {ll / n:.4f}")
