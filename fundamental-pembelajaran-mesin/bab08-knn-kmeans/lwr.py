"""Locally weighted regression dengan kernel Gaussian (Bab 8, Kode 8.3)."""
import numpy as np


def lwr(X, y, x_q, h=0.5):
    """Satu garis lokal per pertanyaan: solusi least squares berbobot."""
    Xb = np.c_[np.ones(len(X)), X]                       # tambah kolom konstanta
    xq = np.r_[1.0, np.atleast_1d(x_q)]
    d2 = ((X - x_q) ** 2).reshape(len(X), -1).sum(axis=1)
    w = np.exp(-d2 / (2 * h ** 2))                        # bobot mengecil bersama jarak
    W = np.diag(w)
    beta = np.linalg.solve(Xb.T @ W @ Xb, Xb.T @ W @ y)   # (X'WX) beta = X'Wy
    return xq @ beta


if __name__ == "__main__":
    # dua puluh titik pada gambar LWR (sin x ditambah noise), h = 0,4
    X = np.round(np.arange(0.2, 6.0, 0.3), 1)
    y = np.array([0.35, 0.38, 0.82, 0.80, 1.05, 0.93, 0.97, 0.66, 0.58, 0.15,
                  0.02, -0.42, -0.55, -0.90, -0.88, -1.08, -0.92, -0.88, -0.58, -0.40])
    h = 0.4
    for q in (1.3, 3.0, 4.7):
        # garis lokal ditulis sebagai b0 + b1 (x - q), sehingga b0 = dugaan di x = q
        Xb = np.c_[np.ones(len(X)), X - q]
        W = np.diag(np.exp(-(X - q) ** 2 / (2 * h ** 2)))
        b0, b1 = np.linalg.solve(Xb.T @ W @ Xb, Xb.T @ W @ y)
        print(f"x_q={q}: garis {b0:.3f} {b1:+.3f}(x - {q}), lwr={lwr(X, y, q, h):.3f}, sin={np.sin(q):.3f}")
