"""Mini-batch SGD dengan penjadwalan learning rate (cosine) pada data sintetis.
Kode 11.3 pada buku."""
import numpy as np


def buat_data(n=10_000, d=5, seed=0):
    rng = np.random.default_rng(seed)
    X = rng.normal(size=(n, d))
    beta_benar = np.arange(1, d + 1, dtype=float)
    y = 3.0 + X @ beta_benar + rng.normal(scale=0.5, size=n)
    return np.column_stack([np.ones(n), X]), y


def eta_cosine(t, T, eta_maks=0.1, eta_min=0.001):
    return eta_min + 0.5 * (eta_maks - eta_min) * (1 + np.cos(np.pi * t / T))


def minibatch_sgd(X, y, ukuran_batch=32, n_epoch=10, seed=0):
    rng = np.random.default_rng(seed)
    n, d = X.shape
    beta = np.zeros(d)
    langkah_per_epoch = int(np.ceil(n / ukuran_batch))
    T = n_epoch * langkah_per_epoch
    t = 0
    for epoch in range(n_epoch):
        urutan = rng.permutation(n)            # acak ulang tiap epoch
        for mulai in range(0, n, ukuran_batch):
            idx = urutan[mulai:mulai + ukuran_batch]
            Xb, yb = X[idx], y[idx]
            g = (2.0 / len(idx)) * Xb.T @ (Xb @ beta - yb)
            beta -= eta_cosine(t, T) * g
            t += 1
        mse = np.mean((X @ beta - y) ** 2)
        print(f"epoch {epoch + 1:2d}  eta={eta_cosine(t, T):.4f}  MSE={mse:.4f}")
    return beta


if __name__ == "__main__":
    X, y = buat_data()
    beta = minibatch_sgd(X, y)
    print("beta SGD     :", beta.round(3))
    print("beta tertutup:", np.linalg.solve(X.T @ X, X.T @ y).round(3))
