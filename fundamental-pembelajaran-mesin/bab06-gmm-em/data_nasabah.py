"""Pembangkit data sintetis segmentasi nasabah (Bab 6).

Dua fitur per nasabah:
  x1 = log10 saldo rata-rata bulanan (rupiah), mis. 6,0 berarti Rp1 juta
  x2 = jumlah transaksi digital per bulan
Tiga segmen dibangkitkan dari tiga Gaussian. Data ini sintetis, bukan data bank nyata.
"""
import numpy as np

SEGMEN = {
    # nama: (banyak, rata-rata, kovarians)
    "aktif-bersaldo-kecil": (250, [5.8, 34.0], [[0.09, 0.60], [0.60, 36.0]]),
    "karyawan-mapan": (200, [6.8, 18.0], [[0.12, -0.50], [-0.50, 16.0]]),
    "prioritas": (50, [7.8, 8.0], [[0.06, 0.0], [0.0, 6.0]]),
}


def buat_data(seed=6):
    rng = np.random.default_rng(seed)
    X, y = [], []
    for k, (n, m, S) in enumerate(SEGMEN.values()):
        X.append(rng.multivariate_normal(m, S, size=n))
        y.append(np.full(n, k))
    X = np.vstack(X)
    X[:, 1] = np.clip(X[:, 1], 0, None)  # transaksi tidak negatif
    return X, np.concatenate(y)


if __name__ == "__main__":
    X, y = buat_data()
    print("bentuk:", X.shape, " banyak per segmen:", np.bincount(y))
    print("rata-rata keseluruhan:", X.mean(axis=0).round(3))
