"""EM untuk Gaussian mixture model dari nol dengan NumPy (Bab 6).

Kovarians penuh, perhitungan dalam ruang log (log-sum-exp), dan regularisasi
kovarians reg_covar seperti pada scikit-learn.
"""
import numpy as np
from scipy.special import logsumexp
from data_nasabah import buat_data
from gaussian_mle import log_gauss


def inisialisasi(X, K, cara, rng):
    """Rata-rata, kovarians, dan bobot awal: 'acak' atau 'kmeans'."""
    n, d = X.shape
    if cara == "acak":       # K titik data acak; kovarians = kovarians seluruh data
        mu = X[rng.choice(n, K, replace=False)]
        Sigma = np.array([np.cov(X.T, bias=True) for _ in range(K)])
        return np.full(K, 1.0 / K), mu, Sigma
    from sklearn.cluster import KMeans      # cara == "kmeans"
    lab = KMeans(K, n_init=10, random_state=0).fit_predict(X)
    pi = np.bincount(lab, minlength=K) / n
    mu = np.array([X[lab == k].mean(axis=0) for k in range(K)])
    Sigma = np.array([np.cov(X[lab == k].T, bias=True) + 1e-6 * np.eye(d)
                      for k in range(K)])
    return pi, mu, Sigma


def em_gmm(X, K, n_iter=500, tol=1e-6, reg_covar=1e-6, seed=0, init="acak"):
    n, d = X.shape
    rng = np.random.default_rng(seed)
    pi, mu, Sigma = inisialisasi(X, K, init, rng)
    riwayat = []
    for it in range(n_iter):
        # E-step: log(pi_k N(x_n|mu_k,Sigma_k)), lalu normalkan per baris
        log_p = np.column_stack([np.log(pi[k]) + log_gauss(X, mu[k], Sigma[k])
                                 for k in range(K)])
        log_px = logsumexp(log_p, axis=1)          # log p(x_n)
        riwayat.append(log_px.sum())               # log-likelihood
        R = np.exp(log_p - log_px[:, None])         # responsibility, n x K
        # M-step
        Nk = R.sum(axis=0)
        pi = Nk / n
        mu = (R.T @ X) / Nk[:, None]
        for k in range(K):
            D = X - mu[k]
            Sigma[k] = (R[:, k, None] * D).T @ D / Nk[k] + reg_covar * np.eye(d)
        if it > 0 and riwayat[-1] - riwayat[-2] < tol:
            break
    return pi, mu, Sigma, R, riwayat


if __name__ == "__main__":
    X, y = buat_data()
    pi, mu, Sigma, R, ll = em_gmm(X, K=3, seed=0)
    print(f"iterasi: {len(ll)}")
    for t in [0, 1, 2, 5, 10, 20, len(ll) - 1]:
        if t < len(ll):
            print(f"  logL iterasi {t:3d}: {ll[t]:.2f}")
    urut = np.argsort(mu[:, 0])
    print("pi   :", pi[urut].round(3))
    print("mu   :\n", mu[urut].round(3))
    for k in urut:
        print("Sigma:", Sigma[k].round(3).tolist())
    print("10 inisialisasi acak (seed 0-9): logL akhir dan banyak iterasi")
    for s in range(10):
        _, _, _, _, l = em_gmm(X, K=3, seed=s)
        print(f"  seed {s}: logL = {l[-1]:.2f}, iterasi = {len(l)}")
    _, mu_km, _, _, l = em_gmm(X, K=3, init="kmeans")
    print(f"inisialisasi K-Means: logL = {l[-1]:.2f}, iterasi = {len(l)}")
    print("  riwayat:", np.round(l, 2).tolist())
    naik = np.all(np.diff(ll) >= -1e-9)
    print("log-likelihood tidak pernah turun:", naik)
    print("seluruh riwayat logL:", np.round(ll, 2).tolist())
