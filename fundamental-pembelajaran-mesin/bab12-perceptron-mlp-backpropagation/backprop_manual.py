"""Satu iterasi backpropagation pada jaringan 2-2-1 (sigmoid, loss 1/2 kuadrat),
persis seperti contoh hitung di buku, lengkap dengan gradient checking.
Kode 9.3 pada buku."""
import numpy as np


def sigmoid(z):
    return 1.0 / (1.0 + np.exp(-z))


x = np.array([1.0, 1.0]); y = 0.0             # contoh XOR (1,1) -> 0
W = np.array([[0.2, -0.3], [0.4, 0.1]])       # baris j = bobot ke neuron tersembunyi j
b = np.array([0.1, -0.2])
v = np.array([0.5, -0.6]); c = 0.3            # lapisan keluaran
eta = 0.5


def maju(W, b, v, c):
    z = W @ x + b; h = sigmoid(z)
    zo = v @ h + c; y_hat = sigmoid(zo)
    return z, h, zo, y_hat, 0.5 * (y_hat - y) ** 2


z, h, zo, y_hat, L = maju(W, b, v, c)
print("forward : z =", z.round(4), "h =", h.round(4), "y_hat =", round(y_hat, 4), "L =", round(L, 4))

# backward: aturan rantai dari keluaran ke masukan
delta_o = (y_hat - y) * y_hat * (1 - y_hat)   # dL/dzo
dv, dc = delta_o * h, delta_o
delta_h = delta_o * v * h * (1 - h)           # dL/dz
dW, db = np.outer(delta_h, x), delta_h
print("delta_o =", round(delta_o, 4), " delta_h =", delta_h.round(4))
print("dv =", dv.round(4), " dW =", dW.round(4).tolist())

# gradient checking untuk satu bobot (W[0,0])
eps = 1e-6
Wp, Wm = W.copy(), W.copy(); Wp[0, 0] += eps; Wm[0, 0] -= eps
numerik = (maju(Wp, b, v, c)[4] - maju(Wm, b, v, c)[4]) / (2 * eps)
print("cek gradien W[0,0]: analitik", round(dW[0, 0], 6), "numerik", round(numerik, 6))

# pembaruan dan forward ulang
W, b, v, c = W - eta * dW, b - eta * db, v - eta * dv, c - eta * dc
print("loss setelah satu langkah:", round(maju(W, b, v, c)[4], 4))
