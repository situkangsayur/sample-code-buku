"""GD, momentum, RMSProp, dan Adam dari nol pada MSE data jam belajar (Bab 8).
Mencetak jumlah iterasi sampai MSE < 0.4801. Kode 10.2 pada buku."""
import numpy as np

x = np.arange(1, 6, dtype=float)
y = np.array([2, 4, 5, 4, 5], dtype=float)
X = np.column_stack([np.ones(5), x])


def grad(b):
    return 2 / 5 * X.T @ (X @ b - y)


def mse(b):
    return np.mean((X @ b - y) ** 2)


def langkah_sgd(b, g, st, eta, t):
    return b - eta * g


def langkah_momentum(b, g, st, eta, t, beta=0.9):
    st["v"] = beta * st.get("v", 0) + g          # kecepatan
    return b - eta * st["v"]


def langkah_rmsprop(b, g, st, eta, t, rho=0.99, eps=1e-8):
    st["s"] = rho * st.get("s", 0) + (1 - rho) * g ** 2
    return b - eta * g / (np.sqrt(st["s"]) + eps)


def langkah_adam(b, g, st, eta, t, b1=0.9, b2=0.999, eps=1e-8):
    st["m"] = b1 * st.get("m", 0) + (1 - b1) * g          # momen pertama
    st["s"] = b2 * st.get("s", 0) + (1 - b2) * g ** 2     # momen kedua
    m_hat = st["m"] / (1 - b1 ** t)                      # koreksi bias
    s_hat = st["s"] / (1 - b2 ** t)
    return b - eta * m_hat / (np.sqrt(s_hat) + eps)


def jalankan(langkah, eta, T=5000):
    b, st = np.zeros(2), {}
    for t in range(1, T + 1):
        b = langkah(b, grad(b), st, eta, t)
        if mse(b) < 0.4801:
            return t, b
    return None, b


for nama, fn, eta in [("GD", langkah_sgd, 0.08), ("momentum", langkah_momentum, 0.01),
                      ("RMSProp", langkah_rmsprop, 0.01), ("Adam", langkah_adam, 0.1)]:
    t, b = jalankan(fn, eta)
    print(f"{nama:9s} eta={eta:<5} iterasi={t}  beta={b.round(3)}")
