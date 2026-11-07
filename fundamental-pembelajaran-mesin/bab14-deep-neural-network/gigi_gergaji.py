"""Fungsi gigi gergaji dari komposisi fungsi tenda yang dibangun dengan dua ReLU.
Kedalaman k memberi 2^k potongan linier dengan hanya 2k neuron. Kode 11.1 pada buku."""
import numpy as np


def relu(z):
    return np.maximum(z, 0.0)


def tenda(x):
    # g(x) = 2x untuk x <= 0.5 dan 2(1 - x) untuk x > 0.5, pada [0, 1]
    return 2 * relu(x) - 4 * relu(x - 0.5)


def jumlah_potongan(y, x):
    kemiringan = np.round(np.diff(y) / np.diff(x), 6)
    return 1 + np.count_nonzero(np.diff(kemiringan))


x = np.linspace(0, 1, 2**12 + 1)
y = x.copy()
for k in range(1, 7):
    y = tenda(y)                         # satu lapisan tersembunyi lagi
    print(f"kedalaman {k}: neuron={2 * k:2d}, potongan linier={jumlah_potongan(y, x)}")
