"""Rantai Markov huruf vokal/konsonan (data Markov 1913, Eugene Onegin).

Angka hitungan pasangan huruf diambil dari ringkasan Hayes (2013):
20.000 huruf, 8.638 vokal, 11.362 konsonan; pasangan vokal-vokal 1.104,
konsonan-konsonan 3.827.
"""
import numpy as np

n_v, n_k = 8638, 11362
vv, kk = 1104, 3827
# Taksiran maximum likelihood: hitung pasangan lalu normalkan per baris
A = np.array([[vv / n_v, 1 - vv / n_v],
              [1 - kk / n_k, kk / n_k]])
np.set_printoptions(precision=4, suppress=True)
print("Matriks transisi (V, K):\n", A)

# Peluang n langkah: baris ke-i dari A^n
for n in (1, 2, 3, 5, 10):
    print(f"A^{n:<2d} baris V = {np.linalg.matrix_power(A, n)[0]}")

# Distribusi stasioner: vektor eigen kiri untuk nilai eigen 1
nilai, vektor = np.linalg.eig(A.T)
s = np.real(vektor[:, np.argmin(abs(nilai - 1))])
s = s / s.sum()
print("Distribusi stasioner:", s)
print("Proporsi vokal pada teks:", round(n_v / (n_v + n_k), 4))
print("Nilai eigen:", np.real(nilai))

# Simulasi: mulai dari vokal, jalankan 100.000 langkah
rng = np.random.default_rng(7)
x, hit = 0, np.zeros(2)
for _ in range(100_000):
    x = rng.choice(2, p=A[x])
    hit[x] += 1
print("Frekuensi simulasi:", hit / hit.sum())
