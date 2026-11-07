"""Kode 13.1 - Self-attention dari nol dengan NumPy.

Memeriksa contoh hitungan Bab 13: dot-product attention tiga kata,
self-attention tiga token (dengan dan tanpa causal mask), dan positional encoding.
"""
import numpy as np


def softmax(s):
    s = s - s.max(axis=-1, keepdims=True)  # cegah overflow
    e = np.exp(s)
    return e / e.sum(axis=-1, keepdims=True)


def self_attention(X, Wq, Wk, Wv, kausal=False, skala=True):
    Q, K, V = X @ Wq, X @ Wk, X @ Wv
    S = Q @ K.T
    if skala:
        S = S / np.sqrt(K.shape[-1])
    if kausal:
        n = S.shape[0]
        S = np.where(np.triu(np.ones((n, n)), k=1) == 1, -np.inf, S)
    A = softmax(S)
    return A @ V, A


def positional_encoding(n, d):
    pe = np.zeros((n, d))
    pos = np.arange(n)[:, None]
    i = np.arange(0, d, 2)
    pe[:, 0::2] = np.sin(pos / 10000 ** (i / d))
    pe[:, 1::2] = np.cos(pos / 10000 ** (i / d))
    return pe


if __name__ == "__main__":
    np.set_printoptions(precision=3, suppress=True)

    print("Dot-product attention, s = (1, 2):")
    H = np.array([[1, 0], [0, 1], [1, 1]], dtype=float)
    s = np.array([1, 2], dtype=float)
    alpha = softmax(H @ s)
    print("  bobot  :", alpha, " konteks:", alpha @ H)

    X = np.array([[1, 0], [0, 1], [1, 1]], dtype=float)
    Wq = np.array([[1, 0], [1, 1]], dtype=float)
    Wk = np.array([[1, 1], [0, 1]], dtype=float)
    Wv = np.array([[1, 0], [0, 2]], dtype=float)

    Z, A = self_attention(X, Wq, Wk, Wv)
    print("Self-attention: A =\n", A, "\nZ =\n", Z)
    Z, A = self_attention(X, Wq, Wk, Wv, kausal=True)
    print("Dengan causal mask: A =\n", A, "\nZ =\n", Z)
    Z, A = self_attention(X, Wq, Wk, Wv, skala=False)
    print("Tanpa pembagian sqrt(d_k): A =\n", A)

    # Permutation equivariance: tukar baris masukan -> baris keluaran ikut tertukar
    perm = [2, 0, 1]
    Z1, _ = self_attention(X, Wq, Wk, Wv)
    Z2, _ = self_attention(X[perm], Wq, Wk, Wv)
    print("Equivariant terhadap permutasi:", np.allclose(Z1[perm], Z2))

    print("Positional encoding d=4, pos=0..3:\n", positional_encoding(4, 4))
