"""K-Means: algoritma Lloyd dan inisialisasi k-means++ dari nol dengan NumPy,
lalu elbow dan silhouette dengan scikit-learn (Bab 8, Kode 8.4 sampai 8.6)."""
import numpy as np
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs
from sklearn.metrics import silhouette_score


def kmeans_lloyd(X, C, maks_iter=100):
    """C: centroid awal (k x d). Mengembalikan centroid, label, dan SSE."""
    C = C.astype(float).copy()
    for it in range(maks_iter):
        d2 = ((X[:, None, :] - C[None, :, :]) ** 2).sum(axis=2)   # jarak kuadrat n x k
        label = d2.argmin(axis=1)                                 # langkah assignment
        sse = d2[np.arange(len(X)), label].sum()
        print(f"iterasi {it + 1}: label={label}, SSE={sse:.3f}")
        C_baru = np.array([X[label == j].mean(axis=0) for j in range(len(C))])  # langkah update
        if np.allclose(C_baru, C):                                # centroid tidak bergerak lagi
            break
        C = C_baru
    return C, label, sse


def kmeanspp_awal(X, k, rng):
    """Pilih k centroid awal dengan peluang sebanding D(x)^2."""
    C = [X[rng.integers(len(X))]]                                 # centroid pertama: acak
    for _ in range(1, k):
        D2 = ((X[:, None, :] - np.array(C)[None]) ** 2).sum(axis=2).min(axis=1)
        C.append(X[rng.choice(len(X), p=D2 / D2.sum())])          # titik jauh lebih mungkin
    return np.array(C)


if __name__ == "__main__":
    # contoh hitungan tangan: enam titik, centroid awal = titik A dan B
    X = np.array([[1, 1], [1.5, 2], [3, 4], [5, 7], [3.5, 5], [4.5, 5]])
    C, label, sse = kmeans_lloyd(X, X[[0, 1]])
    print("centroid akhir:", C)

    # k-means++ pada data yang sama: pusat awal cenderung berada di kelompok berbeda
    C0 = kmeanspp_awal(X, 2, np.random.default_rng(0))
    print("centroid awal k-means++:", C0)
    kmeans_lloyd(X, C0)

    # memilih k: elbow (inertia = SSE) dan silhouette pada data sintetis 4 kelompok
    X, _ = make_blobs(n_samples=300, centers=4, cluster_std=0.8, random_state=0)
    for k in range(2, 9):
        km = KMeans(n_clusters=k, init="k-means++", n_init=10, random_state=0).fit(X)
        print(f"k={k}  inertia={km.inertia_:7.1f}  silhouette={silhouette_score(X, km.labels_):.3f}")
