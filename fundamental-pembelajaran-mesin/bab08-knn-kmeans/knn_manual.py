"""kNN dari nol dengan NumPy: suara biasa dan suara terbobot jarak (Bab 8, Kode 8.1)."""
import numpy as np
from collections import Counter


def knn_prediksi(X_latih, y_latih, x_q, k=5, terbobot=False):
    d = np.sqrt(((X_latih - x_q) ** 2).sum(axis=1))      # jarak Euclidean ke semua data
    idx = np.argpartition(d, k - 1)[:k]                     # k terdekat, O(n)
    suara = Counter()
    for i in idx:
        bobot = 1.0 / max(d[i], 1e-12) ** 2 if terbobot else 1.0
        suara[y_latih[i]] += bobot
    return suara.most_common(1)[0][0], dict(suara)


if __name__ == "__main__":
    hijau = [(4.3, 5.5), (4.6, 4.3), (5.8, 5.4), (3.0, 6.6), (2.6, 4.2), (3.6, 2.8), (4.0, 6.8), (5.2, 2.4)]
    merah = [(5.3, 5.5), (6.2, 5.4), (7.0, 6.4), (7.4, 4.0), (6.6, 2.6), (8.0, 5.8), (6.4, 7.2)]
    X = np.array(hijau + merah)
    y = np.array(["hijau"] * len(hijau) + ["merah"] * len(merah))
    q = np.array([5.0, 5.0])
    for k in (1, 5):
        print(f"k={k}:", knn_prediksi(X, y, q, k))
    print("k=5 terbobot:", knn_prediksi(X, y, q, 5, terbobot=True))
