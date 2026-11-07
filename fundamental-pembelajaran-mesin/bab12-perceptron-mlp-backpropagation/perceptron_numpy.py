"""Perceptron Rosenblatt dari nol: berhasil pada AND dan OR, gagal pada XOR.
Kode 9.1 pada buku."""
import numpy as np


def latih_perceptron(X, y, eta=1.0, max_epoch=20):
    w, b = np.zeros(X.shape[1]), 0.0
    for epoch in range(1, max_epoch + 1):
        salah = 0
        for xi, yi in zip(X, y):
            y_hat = 1 if xi @ w + b > 0 else 0   # fungsi tangga
            if y_hat != yi:                      # hanya belajar saat salah
                w += eta * (yi - y_hat) * xi
                b += eta * (yi - y_hat)
                salah += 1
        if salah == 0:
            return w, b, epoch                   # konvergen
    return w, b, None                            # tidak konvergen


X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]], dtype=float)
for nama, y in [("AND", [0, 0, 0, 1]), ("OR", [0, 1, 1, 1]), ("XOR", [0, 1, 1, 0])]:
    w, b, ep = latih_perceptron(X, np.array(y))
    status = f"konvergen pada epoch {ep}" if ep else "TIDAK konvergen"
    print(f"{nama}: w={w}, b={b}, {status}")
