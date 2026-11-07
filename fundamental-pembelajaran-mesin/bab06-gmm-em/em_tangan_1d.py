"""Contoh hitungan tangan EM untuk GMM 1D dua komponen (Bab 6).

Data: 1, 2, 3, 6, 7, 8. Inisialisasi: pi = (0,5; 0,5), mu = (2; 4), var = (1; 1).
Skrip mencetak setiap langkah agar dapat dicocokkan dengan tabel di buku.
"""
import numpy as np

x = np.array([1.0, 2.0, 3.0, 6.0, 7.0, 8.0])
pi = np.array([0.5, 0.5])
mu = np.array([2.0, 4.0])
var = np.array([1.0, 1.0])


def normal_pdf(x, mu, var):
    return np.exp(-(x - mu) ** 2 / (2 * var)) / np.sqrt(2 * np.pi * var)


def log_likelihood(x, pi, mu, var):
    p = pi * normal_pdf(x[:, None], mu, var)
    return np.log(p.sum(axis=1)).sum()


np.set_printoptions(precision=4, suppress=True)
print(f"iterasi 0: logL = {log_likelihood(x, pi, mu, var):.4f}")
for it in range(1, 31):
    # E-step: responsibility r[n, k]
    dens = normal_pdf(x[:, None], mu, var)          # N(x_n | mu_k, var_k)
    berbobot = pi * dens                             # pi_k N(...)
    r = berbobot / berbobot.sum(axis=1, keepdims=True)
    # M-step
    Nk = r.sum(axis=0)
    pi = Nk / len(x)
    mu = (r * x[:, None]).sum(axis=0) / Nk
    var = (r * (x[:, None] - mu) ** 2).sum(axis=0) / Nk
    ll = log_likelihood(x, pi, mu, var)
    if it <= 2:
        print(f"\n--- iterasi {it} ---")
        print("densitas N(x|mu1,var1):", dens[:, 0])
        print("densitas N(x|mu2,var2):", dens[:, 1])
        print("r1:", r[:, 0])
        print("r2:", r[:, 1])
        print("N_k:", Nk, " pi:", pi, " mu:", mu, " var:", var)
    print(f"iterasi {it}: logL = {ll:.4f}")
    if it > 1 and abs(ll - ll_lama) < 1e-6:
        break
    ll_lama = ll
print("\nakhir: pi", pi, "mu", mu, "var", var)
