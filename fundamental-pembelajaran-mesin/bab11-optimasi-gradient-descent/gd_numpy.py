"""Gradient descent dari nol untuk regresi linier, dibandingkan dengan solusi
bentuk tertutup (persamaan normal). Kode 11.1 pada buku."""
import numpy as np


def mse(X, y, beta):
    e = X @ beta - y
    return np.mean(e ** 2)


def grad_mse(X, y, beta):
    # gradien MSE: (2/n) X^T (X beta - y)
    n = X.shape[0]
    return (2.0 / n) * X.T @ (X @ beta - y)


def gradient_descent(X, y, eta=0.05, n_iter=2000, tol=1e-10):
    beta = np.zeros(X.shape[1])          # titik awal
    riwayat = [mse(X, y, beta)]
    riwayat_beta = [beta.copy()]
    for t in range(n_iter):
        g = grad_mse(X, y, beta)
        if np.linalg.norm(g) < tol:      # kriteria berhenti
            break
        beta = beta - eta * g            # satu langkah turun
        riwayat.append(mse(X, y, beta))
        riwayat_beta.append(beta.copy())
    return beta, riwayat, riwayat_beta


def bentuk_tertutup(X, y):
    # solve lebih stabil daripada menghitung invers secara eksplisit
    return np.linalg.solve(X.T @ X, X.T @ y)


if __name__ == "__main__":
    # data lima titik (jam belajar, nilai kuis) dari Bab 10
    x = np.array([1, 2, 3, 4, 5], dtype=float)
    y = np.array([2, 4, 5, 4, 5], dtype=float)
    X = np.column_stack([np.ones_like(x), x])   # kolom 1 untuk intersep

    beta_gd, riwayat, riwayat_beta = gradient_descent(X, y, eta=0.05)
    # keluaran yang dikutip di awal bab
    for t in (0, 1, 2, 10, 50, 100, 500):
        print(f"iterasi {t:3d}   beta = {riwayat_beta[t].round(4)}   MSE = {riwayat[t]:7.4f}")
    print("GD          :", beta_gd.round(4), "MSE", round(riwayat[-1], 4))
    print("tertutup    :", bentuk_tertutup(X, y).round(4))

    # pengaruh learning rate: batas stabil eta < 2 / lambda_max
    H = (2.0 / len(x)) * X.T @ X
    lam = np.linalg.eigvalsh(H)
    print("eigen Hessian:", lam.round(4), "batas eta:", round(2 / lam.max(), 4))
    for eta in (0.01, 0.05, 0.08, 0.09):
        b, r, _ = gradient_descent(X, y, eta=eta, n_iter=100)
        print(f"eta={eta:<5} MSE setelah 100 iterasi = {r[-1]:.4g}")
