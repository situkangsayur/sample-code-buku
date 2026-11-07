"""Kode 12.1 - Konvolusi dua dimensi dan max pooling dari nol dengan NumPy.

Memeriksa contoh hitungan pada Bab 12 (Gambar 12.2, contoh padding-stride,
contoh detektor tepi, dan contoh pooling Gambar 12.6).
"""
import numpy as np


def conv2d(x, w, b, stride=1, padding=0):
    """x: (C_in, H, W), w: (C_out, C_in, k, k), b: (C_out,)"""
    c_out, c_in, k, _ = w.shape
    assert x.shape[0] == c_in, "jumlah kanal masukan tidak cocok"
    x = np.pad(x, ((0, 0), (padding, padding), (padding, padding)))
    h_out = (x.shape[1] - k) // stride + 1
    w_out = (x.shape[2] - k) // stride + 1
    y = np.zeros((c_out, h_out, w_out))
    for o in range(c_out):
        for i in range(h_out):
            for j in range(w_out):
                petak = x[:, i * stride:i * stride + k, j * stride:j * stride + k]
                y[o, i, j] = np.sum(petak * w[o]) + b[o]
    return y


def max_pool2d(x, k=2, stride=2):
    """x: (C, H, W). Mengambil nilai maksimum tiap petak k x k."""
    c, h, w = x.shape
    h_out = (h - k) // stride + 1
    w_out = (w - k) // stride + 1
    y = np.zeros((c, h_out, w_out))
    for i in range(h_out):
        for j in range(w_out):
            petak = x[:, i * stride:i * stride + k, j * stride:j * stride + k]
            y[:, i, j] = petak.reshape(c, -1).max(axis=1)
    return y


def relu(x):
    return np.maximum(x, 0)


if __name__ == "__main__":
    X = np.array([[1, 2, 0, 1, 3], [0, 1, 3, 2, 1], [2, 1, 0, 1, 0],
                  [1, 0, 2, 3, 1], [0, 2, 1, 0, 2]], dtype=float)[None]  # (1,5,5)
    K = np.array([[1, 0, -1]] * 3, dtype=float)[None, None]           # (1,1,3,3)
    nol = np.zeros(1)

    print("Konvolusi valid, stride 1 (Gambar 12.2):")
    Y = conv2d(X, K, nol)
    print(Y[0])
    print("Setelah ReLU:")
    print(relu(Y)[0])

    print("Padding 1, stride 2:")
    print(conv2d(X, K, nol, stride=2, padding=1)[0])

    print("Detektor tepi pada citra 6x6 (separuh terang, separuh gelap):")
    tepi = np.tile([10, 10, 10, 0, 0, 0], (6, 1)).astype(float)[None]
    print(conv2d(tepi, K, nol)[0])

    print("Max pooling 2x2 stride 2 (Gambar 12.6):")
    F = np.array([[1, 3, 2, 1], [4, 6, 5, 0], [3, 1, 1, 2], [0, 2, 7, 4]], dtype=float)[None]
    print(max_pool2d(F)[0])

    # Jumlah parameter Conv2d(3, 16, 3): 16 * 27 + 16 = 448
    w = np.zeros((16, 3, 3, 3))
    print("Parameter Conv2d(3,16,3):", w.size + 16)
