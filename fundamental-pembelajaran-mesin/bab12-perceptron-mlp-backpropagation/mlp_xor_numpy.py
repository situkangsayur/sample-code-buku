"""MLP 2-4-1 dari nol dengan NumPy untuk masalah XOR: forward, backward,
dan mini-batch penuh. Kode 9.5 pada buku."""
import numpy as np

rng = np.random.default_rng(0)
X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]], dtype=float)
y = np.array([[0], [1], [1], [0]], dtype=float)


def sigmoid(z):
    return 1 / (1 + np.exp(-z))


# inisialisasi acak kecil (Xavier sederhana), bias nol
H = 4
W1 = rng.normal(0, np.sqrt(1 / 2), size=(2, H)); b1 = np.zeros(H)
W2 = rng.normal(0, np.sqrt(1 / H), size=(H, 1)); b2 = np.zeros(1)
eta = 1.0

for epoch in range(5001):
    # forward pass (baris = contoh)
    A1 = np.tanh(X @ W1 + b1)
    P = sigmoid(A1 @ W2 + b2)
    loss = -np.mean(y * np.log(P) + (1 - y) * np.log(1 - P))
    # backward pass
    dZ2 = (P - y) / len(X)                  # sigmoid + BCE
    dW2 = A1.T @ dZ2; db2 = dZ2.sum(0)
    dZ1 = (dZ2 @ W2.T) * (1 - A1 ** 2)      # turunan tanh
    dW1 = X.T @ dZ1; db1 = dZ1.sum(0)
    # pembaruan
    W1 -= eta * dW1; b1 -= eta * db1
    W2 -= eta * dW2; b2 -= eta * db2
    if epoch % 1000 == 0:
        print(f"epoch {epoch:4d}  loss {loss:.4f}")

print("prediksi:", P.ravel().round(3))
