"""Kode 1.1: regresi linier dengan bentuk tertutup (normal equation)
dan dengan gradient descent, pada data yang sama."""
import numpy as np


def main():
    # Data contoh: tiga titik (x, y)
    x = np.array([1.0, 2.0, 3.0])
    y = np.array([2.0, 3.0, 5.0])
    X = np.column_stack([np.ones_like(x), x])  # kolom 1 untuk intercept

    # 1) Analitik: normal equation (pakai solve, bukan inv, agar stabil)
    beta_analitik = np.linalg.solve(X.T @ X, X.T @ y)

    # 2) Numerik: gradient descent pada rata-rata kuadrat galat (MSE)
    beta = np.zeros(2)
    eta = 0.1
    for t in range(2000):
        galat = X @ beta - y
        grad = 2 * X.T @ galat / len(y)  # turunan MSE terhadap beta
        beta -= eta * grad

    print("analitik:", beta_analitik)  # [0.3333 1.5]
    print("numerik :", beta)  # sangat dekat dengan di atas


if __name__ == "__main__":
    main()
